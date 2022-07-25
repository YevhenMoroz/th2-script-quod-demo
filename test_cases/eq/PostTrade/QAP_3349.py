import logging
import time
from datetime import datetime, timedelta
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


class QAP_3349(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client('client_pt_1')  # MOClient
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.settl_date = datetime.strftime(datetime.now(), '%#m/%#d/%Y')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
            response = self.fix_manager.send_message_and_receive_response(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
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
        self.middle_office.set_modify_ticket_details(settl_type='Regular', settl_date=self.settl_date,
                                                     settl_currency='UAH', exchange_rate='2',
                                                     exchange_rate_calc='Multiply', pset='CREST')
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Checking values after the Book in Middle Office
        values_after_book = self.middle_office.extract_list_of_block_fields(
            ['SettlDate', MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value, MiddleOfficeColumns.settltype.value,
             MiddleOfficeColumns.settl_currency.value, MiddleOfficeColumns.exchange_rate.value,
             MiddleOfficeColumns.settl_curr_fx_rate_calc.value, MiddleOfficeColumns.pset.value,
             MiddleOfficeColumns.pset_bic.value], [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {'SettlDate': self.settl_date, MiddleOfficeColumns.sts.value: 'ApprovalPending',
             MiddleOfficeColumns.match_status.value: 'Unmatched', MiddleOfficeColumns.summary_status.value: '',
             MiddleOfficeColumns.settltype.value: 'Regular', MiddleOfficeColumns.settl_currency.value: 'UAH',
             MiddleOfficeColumns.exchange_rate.value: '2', MiddleOfficeColumns.settl_curr_fx_rate_calc.value: 'M',
             MiddleOfficeColumns.pset.value: 'CREST', MiddleOfficeColumns.pset_bic.value: 'TESTBIC'}, values_after_book,
            'Comparing values after Book for block of MiddleOffice')
        # endregion

        # region Amend block and checking values after it in the Amend ticket
        settl_date_amend = datetime.strftime(datetime.now() + timedelta(days=1), '%#m/%#d/%Y')
        self.middle_office.set_modify_ticket_details(settl_type='Regular', settl_date=settl_date_amend,
                                                     settl_currency='USD', exchange_rate='4',
                                                     exchange_rate_calc='Divide', pset='EURO_CLEAR', toggle_manual=True,
                                                     remove_comm=True, remove_fee=True, extract_book=True)
        extract_amend = self.middle_office.amend_block([OrderBookColumns.order_id.value, order_id])
        # endregion

        # region Checking values in the Amend ticket
        actual_values = {'Net Price': extract_amend.get('book.netPrice'),
                         'Net Amount': extract_amend.get('book.netAmount'),
                         MiddleOfficeColumns.client_comm.value: extract_amend.get('book.totalComm'),
                         MiddleOfficeColumns.total_fees.value: extract_amend.get('book.totalFees'),
                         'Gross amount': extract_amend.get('book.grossAmount'),
                         MiddleOfficeColumns.pset_bic.value: extract_amend.get('book.psetBic'),
                         MiddleOfficeColumns.exchange_rate.value: extract_amend.get('book.exchangeRate'),
                         MiddleOfficeColumns.settltype.value: extract_amend.get('book.settlementType')}
        expected_values = {'Net Price': '10', 'Net Amount': '1,000', MiddleOfficeColumns.client_comm.value: '0',
                           MiddleOfficeColumns.total_fees.value: '0', 'Gross amount': '1,000',
                           MiddleOfficeColumns.pset_bic.value: 'MGTCBEBE',
                           MiddleOfficeColumns.exchange_rate.value: '4', MiddleOfficeColumns.settltype.value: 'Regular'}
        self.middle_office.compare_values(expected_values, actual_values, 'Comparing values in Amend ticket')
        # endregion

        # region Checking values after the Amend in Middle Office
        values_after_amend = self.middle_office.extract_list_of_block_fields(
            ['SettlDate', MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value, MiddleOfficeColumns.settltype.value,
             MiddleOfficeColumns.settl_currency.value, MiddleOfficeColumns.exchange_rate.value,
             MiddleOfficeColumns.settl_curr_fx_rate_calc.value, MiddleOfficeColumns.total_fees.value, 'Net Amt',
             'Net Price', MiddleOfficeColumns.pset.value, MiddleOfficeColumns.pset_bic.value],
            [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {'SettlDate': settl_date_amend, MiddleOfficeColumns.sts.value: 'ApprovalPending',
             MiddleOfficeColumns.match_status.value: 'Unmatched', MiddleOfficeColumns.summary_status.value: '',
             MiddleOfficeColumns.settltype.value: 'Regular', MiddleOfficeColumns.settl_currency.value: 'USD',
             MiddleOfficeColumns.exchange_rate.value: '4', MiddleOfficeColumns.settl_curr_fx_rate_calc.value: 'D',
             'Net Amt': '1,000', 'Net Price': '10', MiddleOfficeColumns.pset.value: 'EURO_CLEAR',
             MiddleOfficeColumns.pset_bic.value: 'MGTCBEBE'}, values_after_amend,
            'Comparing values after Amend for block of MiddleOffice')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
