import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_5614(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price_first = '19.2'
        self.price_second = '18.89'
        self.price_third = '19'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message_first = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_second = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message_third = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            # first order
            trade_rule_first = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(
                                                                                                      self.price_first),
                                                                                                  int(self.qty), 0)
            self.fix_message_first.set_default_dma_limit()
            self.fix_message_first.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client,
                 'Price': self.price_first})
            response_first = self.fix_manager.send_message_and_receive_response(self.fix_message_first)

            # second order
            trade_rule_second = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                                   self.venue_client_names,
                                                                                                   self.venue,
                                                                                                   float(
                                                                                                       self.price_second),
                                                                                                   int(self.qty), 0)
            self.fix_message_second.set_default_dma_limit()
            self.fix_message_second.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client,
                 'Price': self.price_second})
            response_second = self.fix_manager.send_message_and_receive_response(self.fix_message_second)
            # get Client Order ID
            cl_ord_id_second = response_second[0].get_parameters()['ClOrdID']

            # third order
            trade_rule_third = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(
                                                                                                      self.price_third),
                                                                                                  int(self.qty), 0)
            self.fix_message_third.set_default_dma_limit()
            self.fix_message_third.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client,
                 'Price': self.price_third})
            response_third = self.fix_manager.send_message_and_receive_response(self.fix_message_third)
            # get Client Order ID
            cl_ord_id_third = response_third[0].get_parameters()['ClOrdID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule_first)
            self.rule_manager.remove_rule(trade_rule_second)
            self.rule_manager.remove_rule(trade_rule_third)
        # endregion

        # region Book of the second and third orders
        self.middle_office.set_modify_ticket_details(selected_row_count=2, extract_book=True)
        extract_book = self.middle_office.book_order()
        # endregion

        # region Comparing Agreed Price after Book of the second and third orders
        agreed_price = extract_book.get('book.agreedPrice')
        self.middle_office.compare_values({'AgreedPrice': '18.945'}, {'AgreedPrice': agreed_price},
                                          'Comparing Agreed Price in the Booking ticket')

        avg_px = self.middle_office.extract_block_field(column_name=MiddleOfficeColumns.price.value)['AvgPx']
        self.middle_office.compare_values({MiddleOfficeColumns.price.value: '18.945'},
                                          {MiddleOfficeColumns.price.value: avg_px},
                                          'Comparing Agreed Price in the Middle office')
        # endregion

        # region Mass Unbook and checking PostTradeStatus in the Order book
        self.order_book.mass_unbook([1, 2])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_third])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value},
            'Comparing PostTradeStatus after Mass Unbook of the first order')
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id_second])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value},
            'Comparing PostTradeStatus after Mass Unbook of the second order')
        # endregion

        # region Book of three orders
        self.middle_office.set_modify_ticket_details(selected_row_count=3, extract_book=True)
        extract_book2 = self.middle_office.book_order()
        # endregion

        # region Comparing AgreedPrice after Book of three orders
        agreed_price2 = extract_book2.get('book.agreedPrice')
        self.middle_office.compare_values({'AgreedPrice': '19.03'}, {'AgreedPrice': agreed_price2},
                                          'Comparing Agreed Price in the Booking ticket')

        avg_px2 = self.middle_office.extract_block_field(column_name=MiddleOfficeColumns.price.value)['AvgPx']
        self.middle_office.compare_values({MiddleOfficeColumns.price.value: '19.03'},
                                          {MiddleOfficeColumns.price.value: avg_px2},
                                          'Comparing Agreed Price in the Middle office')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
