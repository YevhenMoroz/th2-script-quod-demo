import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import Connectivity
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_2003(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = Connectivity.Ganymede_317_ss.value
        self.bs_connectivity = Connectivity.Ganymede_317_bs.value
        self.qty = '500'
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.sts = None
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingle_Market_FIXStandard(self.bs_connectivity,
                                                                             self.venue_client_names, self.venue,
                                                                             True, 0, 0)
            self.fix_message.set_default_dma_market()
            self.fix_message.change_parameters({'Side': '2', 'TimeInForce': '6'})
            self.fix_message.add_tag({'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d")})
            self.fix_message.update_fields_in_component('OrderQtyData', {'OrderQty': self.qty})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Set-up parameters for ExecutionReports
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.remove_parameter('Price')
        self.exec_report.change_parameters(
            {'ReplyReceivedTime': '*', 'SecondaryOrderID': '*', 'Text': '*', 'ExpireDate': '*'})
        # endregion

        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Check values in OrderBook
        sts = self.order_book.extract_field(OrderBookColumns.sts.value)
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.eliminated.value},
                                       {OrderBookColumns.sts.value: sts}, 'Checking order status in the order book')
        # endregion
        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
