import logging
import time
from pathlib import Path

from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7356(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.order_submit = OrderSubmitOMS(data_set)
        self.cancel_request = CancelOrderRequest()
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.dfd_batch = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameters()["ClOrdID"]
        # endregion

        # region do split order
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            self.order_submit.set_default_child_dma(order_id, cl_ord_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_3")}]},
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_2")})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region get child DMA id
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        child_ord_id = ord_reply_block['OrdID']
        # endregion

        # region cancel dma order
        cancel_rule = None
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.fix_env.buy_side,
                                                                               self.client_for_rule,
                                                                               self.mic, True)
            self.cancel_request.set_default(child_ord_id)
            self.java_api_manager.send_message_and_receive_response(self.cancel_request)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            self.rule_manager.remove_rule(cancel_rule)
        # endregion

        # region check cancellation
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.TransStatus_CXL.value},
                                             ord_reply_block, 'Check child order after cancellation')
        # endregion

        # region manual exec
        self.trade_entry_request.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check execution
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report_block, 'Check execution of parent order')
        # endregion

        # region complete order
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        # endregion

        # region check complete
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value},
            exec_report_block, 'Check completing of parent order')
        # endregion
