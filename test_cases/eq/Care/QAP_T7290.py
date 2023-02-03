import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7290(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.venue_client = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.client = self.data_set.get_client('client_1')  # MOClient
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.suspend_order = SuspendOrderManagementRequest()
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.qty = '100'
        self.price = '20'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 : create CO order via FIX
        self.fix_message.change_parameters(
            {'Account': self.client, 'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region step 2: create Child order:
        nos_rule = None
        child_order_id = None
        listing = self.data_set.get_listing_id_by_name("listing_3")
        instrument = self.data_set.get_instrument_id_by_name("instrument_2")
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.venue_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            self.order_submit.set_default_child_dma(order_id, order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                                 "Price": self.price,
                                                                                 'OrdQty': self.qty,
                                                                                 'ExecutionPolicy': 'DMA',
                                                                                 'InstrID': instrument,
                                                                                 'ListingList': {'ListingBlock':
                                                                                     [{
                                                                                         'ListingID': listing}]}
                                                                                 })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_order_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Checking expected and actually result (step 2)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 3 step 4: Suspend CO order
        self.suspend_order.set_default(order_id)
        self.java_api_manager.send_message_and_receive_response(self.suspend_order)
        suspend_reply = \
            self.java_api_manager.get_last_message(
                ORSMessageType.SuspendOrderManagementReply.value).get_parameters()[
                JavaApiFields.SuspendOrderManagementReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.SuspendedCare.value: 'Y',
                                              JavaApiFields.OrdID.value: order_id},
                                             suspend_reply,
                                             f'Checking that parent order has {JavaApiFields.SuspendedCare.value} = "Y" (step 4)')
        # endregion

        # region step 5: Trade Child DMA order
        self.execution_report.set_default_trade(child_order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "OrdQty": self.qty,
            "LastTradedQty": self.qty,
            "LastPx": self.price,
            "Price": self.price,
            "LeavesQty": '0',
            "CumQty": self.qty,
            "AvgPrice": self.price

        })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        expected_result = ExecutionReportConst.TransExecStatus_FIL.value
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.TransExecStatus.value]
        self.java_api_manager.compare_values({JavaApiFields.TransExecStatus.value: expected_result},
                                             {JavaApiFields.TransExecStatus.value: actually_result},
                                             'Checking that Child order fully executed (step 5)')
        # endregion
