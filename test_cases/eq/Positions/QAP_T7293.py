import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import \
    ManualMatchExecToParentOrdersRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderActionRequest import OrderActionRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7293(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.action_request = OrderActionRequest()
        self.order_submit = OrderSubmitOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.unmatch_request = UnMatchRequest()
        self.match_request = ManualMatchExecToParentOrdersRequest()
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.dfd_manag_batch = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_ord_id = response[0].get_parameter("ClOrdID")
        # endregion

        # region split order
        trd_qty = int(self.qty) // 2
        trade_rule = None
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(trd_qty), 1)
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_2"), 'ClOrdID': cl_ord_id})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region check values
        child_order_id = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value).get_parameter(JavaApiFields.OrdReplyBlock.value)['OrdID']
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        parent_exec_id1 = exec_report[JavaApiFields.ExecID.value]
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, child_order_id).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        child_exec_id = exec_report[JavaApiFields.ExecID.value]
        # endregion

        # region unmatch execution
        self.unmatch_request.set_default(self.data_set, parent_exec_id1, str(trd_qty))
        self.java_api_manager.send_message_and_receive_response(self.unmatch_request)
        # endregion

        # region check values
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, order_id).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value},
                                             exec_report, "Check Exec sts after UnMatch action")
        # endregion

        # region check values on Sell-side gtw
        ignored_list = ['GatingRuleCondName', 'GatingRuleName', 'VenueType', 'TradeDate', 'LastMkt', 'Parties',
                        'QuodTradeQualifier', 'BookID', 'TradeReportingIndicator', 'NoParty', 'tag5120',
                        'SecondaryOrderID', 'ExecBroker']
        self.exec_report.set_default_trade_cancel(self.fix_message)
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion
