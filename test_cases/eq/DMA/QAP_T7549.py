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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7549(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '1300'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # XPAR_CLIENT1
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameters(
            {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}})
        self.price = self.fix_message.get_parameter('Price')
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
       # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create TIF=Day DMA order via FIX and execute it
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']
            order_id = response[0].get_parameters()['OrderID']
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region check execution report 39=0
        list_to_ignor_new = ['SecondaryOrderID', 'LastMkt', 'Text']
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_to_ignor_new)
        # endregion
        # region check execution report 39=2
        list_to_ignor_filled = ['ReplyReceivedTime', 'SettlCurrency', 'Text', 'LastMkt', 'SecurityDesc']
        self.exec_report.set_default_filled(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ignored_fields=list_to_ignor_filled)
        # endregion