import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7445(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # XPAR_CLIENT1
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        self.fix_message.set_default_dma_limit()
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.fix_message.change_parameters(
            {'TimeInForce': '1'})
        self.dfd_manager = DFDManagementBatchOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        order_id = None
        trade_rule = None
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity,
                self.venue_client_names,
                self.venue,
                float(self.price),
                int(int(self.qty) / 2), 0)

            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region complete order
        self.dfd_manager.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.dfd_manager)
        self.__return_result(responses, ORSMessageType.OrderReply.value)
        ord_reply_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_DFD.value},
                                             ord_reply_block, "Check order sts after Complete action")
        # endregion

        # region notifying DFD order
        self.dfd_manager.set_notify_DFD(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.dfd_manager)
        self.__return_result(responses, ORSMessageType.OrderReply.value)
        ord_reply_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_DFD.value},
                                             ord_reply_block, "Check order sts after Notify DFD action")
        # endregion

        # region checking execution report (150=0) in BO
        ignored_list = ['Parties', 'QuodTradeQualifier', 'BookID', 'NoParty', 'SecondaryOrderID', 'tag5120', 'LastMkt',
                        'Text', 'ExecBroker', 'ReplyReceivedTime', "GatingRuleCondName", "GatingRuleName"]
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion

        # region checking execution report (150=3) in BO
        ignored_list = ['SettlCurrency', 'LastExecutionPolicy', 'TradeDate', 'TradeReportingIndicator', 'LastMkt',
                        'SecurityDesc', 'SecondaryExecID', 'ExDestination', 'GrossTradeAmt', "GatingRuleCondName",
                        "GatingRuleName","ProductComplex"]
        self.fix_message.update_fields_in_component("Instrument", {"SecurityExchange": self.mic})
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters({"ExecType": '3', "OrdStatus": '1'})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
