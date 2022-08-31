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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7228(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '20'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.venue,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 1)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Filter Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        # endregion

        # region Check values in OrderBook
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after trading')
        # endregion

        # region Book order and checking values after it in the Order book
        self.middle_office.set_modify_ticket_details(settl_type='Regular', settl_currency='UAH', exchange_rate='2',
                                                     exchange_rate_calc='Multiply', toggle_recompute=True,
                                                     toggle_manual=True, remove_comm=True, remove_fee=True,
                                                     extract_book=True)
        extract_book = self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Checking the values after the Book in the Middle Office
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value,
                                                          [MiddleOfficeColumns.order_id.value, order_id])
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.price.value, MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.settl_currency.value, 'Gross Amt', 'Net Price'],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        agreed_price = str(round(int(self.price) * 2))
        gross_amount = str(int(agreed_price) * int(self.qty))
        gross_amount_format = '{:,}'.format(int(gross_amount))
        net_price = str(round(int(gross_amount) / int(self.qty)))
        self.middle_office.compare_values(
            {MiddleOfficeColumns.price.value: agreed_price, MiddleOfficeColumns.sts.value: 'ApprovalPending',
             MiddleOfficeColumns.match_status.value: 'Unmatched', MiddleOfficeColumns.settl_currency.value: 'UAH',
             'Gross Amt': gross_amount_format, 'Net Price': net_price}, values_after_book,
            'Comparing values after Book for block of MiddleOffice')
        # endregion

        # region Amend block and checking values after it in the Amend ticket
        self.middle_office.set_modify_ticket_details(extract_book=True)
        extract_amend = self.middle_office.amend_block(
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        actual_values = {'Gross amount': extract_amend.get('book.grossAmount'),
                         'Agreed price': extract_amend.get('book.agreedPrice')}
        expected_values = {'Gross amount': extract_book.get('book.grossAmount'),
                           'Agreed price': extract_book.get('book.agreedPrice')}
        self.middle_office.compare_values(expected_values, actual_values, 'Comparing values after Amend')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
