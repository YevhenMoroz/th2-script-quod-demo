import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelReplaceRequestOMS import \
    FixMessageOrderCancelReplaceRequestOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7613(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '500'
        self.price = '20'
        self.price_amend = '19'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # XPAR_CLIENT1
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_amend = FixMessageOrderCancelReplaceRequestOMS(self.data_set)
        self.fix_message_cancel = FixMessageOrderCancelRequestOMS()
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters({'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Set-up parameters for ExecutionReports and chack it
        ignored_list = ['ReplyReceivedTime', 'ReplyReceivedTime', 'Text', 'LastMkt', 'SecondaryOrderID'
                        ,"GatingRuleCondName", "GatingRuleName"]
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion

        # region Amend order
        try:
            nos_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                                   self.venue_client_names,
                                                                                   self.venue, True)
            self.fix_message_amend.set_default(self.fix_message)
            self.fix_message_amend.change_parameter('Price', self.price_amend)
            self.fix_manager.send_message_fix_standard(self.fix_message_amend)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region ExecReport Replaced
        ignored_list = ['ReplyReceivedTime', 'ReplyReceivedTime', 'Text', 'LastMkt', 'SecondaryOrderID', 'SettlType',
                        'SecurityDesc',"GatingRuleCondName", "GatingRuleName","ProductComplex"]
        self.exec_report.set_default_replaced(self.fix_message)
        self.exec_report.change_parameter('Price', self.price_amend)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion

        # region Cancelling order
        try:
            nos_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity,
                                                                            self.venue_client_names,
                                                                            self.venue, True)
            self.fix_message_cancel.set_default(self.fix_message)
            self.fix_manager.send_message_fix_standard(self.fix_message_cancel)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region ExecReport Cancelled
        ignored_list = ['ReplyReceivedTime', 'ReplyReceivedTime', 'Text', 'LastMkt', 'SecondaryOrderID', 'SettlType',
                        'SecurityDesc', 'CxlQty',"GatingRuleCondName", "GatingRuleName","ProductComplex"]
        self.exec_report.set_default_canceled(self.fix_message)
        self.exec_report.change_parameter('Price', self.price_amend)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=ignored_list)
        # endregion
