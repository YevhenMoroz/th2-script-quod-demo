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
    MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7495(TestCase):
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
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')  # MOClient_SA1
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

        # region Filter and check values in Order Book
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after trading')
        # endregion

        # region Book order and checking values after it in the Order book
        self.middle_office.set_modify_ticket_details(settl_type='Regular', settl_date=self.settl_date,
                                                     settl_currency='UAH', exchange_rate='2',
                                                     exchange_rate_calc='Multiply', pset='CREST',
                                                     toggle_manual=True, remove_comm=True, remove_fee=True,
                                                     comm_basis='Absolute', comm_rate='5', fee_type='Regulatory',
                                                     fee_basis='Absolute', fee_rate='5')
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
             MiddleOfficeColumns.settl_curr_fx_rate_calc.value, MiddleOfficeColumns.total_fees.value, 'Net Amt',
             'Net Price', MiddleOfficeColumns.pset.value, MiddleOfficeColumns.pset_bic.value,
             MiddleOfficeColumns.client_comm.value], [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {'SettlDate': self.settl_date, MiddleOfficeColumns.sts.value: 'ApprovalPending',
             MiddleOfficeColumns.match_status.value: 'Unmatched', MiddleOfficeColumns.summary_status.value: '',
             MiddleOfficeColumns.settltype.value: 'Regular', MiddleOfficeColumns.settl_currency.value: 'UAH',
             MiddleOfficeColumns.exchange_rate.value: '2', MiddleOfficeColumns.settl_curr_fx_rate_calc.value: 'M',
             MiddleOfficeColumns.total_fees.value: '5', 'Net Amt': '1,010', 'Net Price': '10.1',
             MiddleOfficeColumns.pset.value: 'CREST', MiddleOfficeColumns.pset_bic.value: 'TESTBIC',
             MiddleOfficeColumns.client_comm.value: '5'}, values_after_book,
            'Comparing values after Book for block of MiddleOffice')
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Checking values after Allocate in Middle Office
        values_after_allocate = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.summary_status.value], [OrderBookColumns.order_id.value, order_id])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: 'Accepted', MiddleOfficeColumns.match_status.value: 'Matched',
             MiddleOfficeColumns.summary_status.value: 'MatchedAgreed'}, values_after_allocate,
            'Checking values after Allocate in Middle Office')
        # endregion

        # region Checking values in Allocations
        extracted_fields = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value])
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: 'Affirmed', AllocationsColumns.match_status.value: 'Matched'},
            extracted_fields, 'Checking values in Allocations')
        # endregion

        # region Amend Allocation
        settl_date_amend = datetime.strftime(datetime.now() + timedelta(days=1), '%#m/%#d/%Y')
        self.middle_office.set_modify_ticket_details(settl_date=settl_date_amend, settl_currency='USD',
                                                     exchange_rate='4', exchange_rate_calc='Divide', pset='EURO_CLEAR',
                                                     remove_comm=True, comm_basis='Absolute', comm_rate='10',
                                                     fee_type='ValueAddedTax', fee_basis='Absolute', fee_rate='5',
                                                     is_alloc_amend=True, extract_alloc=True)
        extract_alloc_ticket = self.middle_office.amend_allocate()
        # endregion

        # region Checking values in the Allocation ticket
        actual_values = {'Net Price': extract_alloc_ticket.get('alloc.netPrice'),
                         'Net Amount': extract_alloc_ticket.get('alloc.netAmount'),
                         MiddleOfficeColumns.client_comm.value: extract_alloc_ticket.get('alloc.totalComm'),
                         MiddleOfficeColumns.total_fees.value: extract_alloc_ticket.get('alloc.totalFees'),
                         'Gross amount': extract_alloc_ticket.get('alloc.grossAmount'),
                         MiddleOfficeColumns.pset_bic.value: extract_alloc_ticket.get('alloc.psetBic'),
                         MiddleOfficeColumns.exchange_rate.value: extract_alloc_ticket.get('alloc.exchangeRate'),
                         MiddleOfficeColumns.settltype.value: extract_alloc_ticket.get('alloc.settlementType')}
        expected_values = {'Net Price': '10.2', 'Net Amount': '1,020', MiddleOfficeColumns.client_comm.value: '10',
                           MiddleOfficeColumns.total_fees.value: '10', 'Gross amount': '1,000',
                           MiddleOfficeColumns.pset_bic.value: 'MGTCBEBE',
                           MiddleOfficeColumns.exchange_rate.value: '4', MiddleOfficeColumns.settltype.value: 'Regular'}
        self.middle_office.compare_values(expected_values, actual_values, 'Comparing values in Amend ticket')
        # endregion

        # region Checking values after the Amend Allocation
        values_after_amend = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value, 'Net Amt', 'Net Price', 'Gross Amt',
             'SettlDate', 'Settl Curr Amt', 'Settl Currency', 'Settl Curr Fx Rate', 'Settl Curr Fx Rate Calc Text',
             AllocationsColumns.pset.value, AllocationsColumns.pset_bic.value, AllocationsColumns.account_id.value,
             AllocationsColumns.total_fees.value, AllocationsColumns.client_comm.value])
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: 'Affirmed', AllocationsColumns.match_status.value: 'Matched',
             'Net Amt': '1,020', 'Net Price': '10.2', 'Gross Amt': '1,000', 'SettlDate': settl_date_amend,
             'Settl Curr Amt': '255', 'Settl Currency': 'USD', 'Settl Curr Fx Rate': '4',
             'Settl Curr Fx Rate Calc Text': 'Divide', AllocationsColumns.pset.value: 'EURO_CLEAR',
             AllocationsColumns.pset_bic.value: 'MGTCBEBE', AllocationsColumns.account_id.value: self.alloc_account,
             AllocationsColumns.total_fees.value: '10', AllocationsColumns.client_comm.value: '10'}, values_after_amend,
            'Comparing values after Amend Allocation')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
