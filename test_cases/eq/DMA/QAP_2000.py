import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager, Simulators
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# region TestData
ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity
qty = '40'


# endregion


class QAP_2000(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        order_book = OMSOrderBook(self.test_id, self.session_id)
        fix_manager = FixManager(ss_connectivity, self.test_id)
        fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_market()
        fix_message.change_parameter('Side', '2')
        fix_message.update_fields_in_component('OrderQtyData', {'OrderQty': qty})
        fix_verifier = FixVerifier(ss_connectivity, self.test_id)
        # endregion
        # region Create DMA order via FIX
        fix_manager.send_message_fix_standard(fix_message)
        try:
            rule_manager = RuleManager(Simulators.equity)
            venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
            venue = self.data_set.get_mic_by_name('mic_1')
            nos_rule = rule_manager.add_NewOrdSingle_Market_FIXStandard(bs_connectivity, venue_client_names, venue,
                                                                        False, int(qty), 0)

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            rule_manager.remove_rule(nos_rule)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_new(fix_message)
        exec_report.remove_parameter('Price')
        exec_report.change_parameters({'ReplyReceivedTime': '*', 'SecondaryOrderID': '*', 'Text': '*'})
        # endregion
        # region Check ExecutionReports
        fix_verifier.check_fix_message_fix_standard(exec_report)
        # endregion
        # region Check values in OrderBook
        sts = order_book.extract_field(OrderBookColumns.sts.value)
        order_book.compare_values({OrderBookColumns.sts.value: ExecSts.eliminated.value},
                                  {OrderBookColumns.sts.value: sts}, 'Checking order status in the order book')
        # endregion
