import logging
import time
from datetime import datetime
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, PostTradeStatuses, \
    MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_5384(TestCase):
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
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
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
                {'Side': '2', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client})
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

        # region Filter Order Book and Check statuses
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing values after trading')
        # endregion

        # region Extracting values from Booking ticket
        extract_main_panel_from_booking = self.order_book.extracting_values_from_booking_ticket(
            [PanelForExtraction.MAIN_PANEL],
            filter_dict={OrderBookColumns.cl_ord_id.value: cl_ord_id})
        values_from_main_panel = {}
        for d in self.middle_office.split_tab_misk(extract_main_panel_from_booking):
            values_from_main_panel.update(d)
        # endregion

        # region Book order and checking values after it in the Order book
        self.middle_office.set_modify_ticket_details(settl_type='Regular', settl_currency='UAH', exchange_rate='2',
                                                     exchange_rate_calc='Multiply', toggle_recompute=True)
        self.middle_office.book_order(filter=[OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value},
            'Comparing PostTradeStatus after Book')
        # endregion

        # region Calculating expected commission and fees
        if len(values_from_main_panel['TotalComm']) == 0:
            values_from_main_panel['TotalComm'] = '0'
        if len(values_from_main_panel['TotalFees']) == 0:
            values_from_main_panel['TotalFees'] = '0'
        expected_fees = str(float(values_from_main_panel['TotalFees']) * 2)
        if expected_fees[-1] == '0':
            expected_fees = str(int(float(expected_fees)))
        expected_comm = str(float(values_from_main_panel['TotalComm']) * 2)
        if expected_comm[-1] == '0':
            expected_comm = str(int(float(expected_comm)))
        # endregion

        # region Checking the values after the Book in the Middle Office
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value,
                                                          [MiddleOfficeColumns.order_id.value, order_id])
        values_after_book = self.middle_office.extract_list_of_block_fields(
            [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value,
             MiddleOfficeColumns.settl_currency.value, MiddleOfficeColumns.exchange_rate.value,
             MiddleOfficeColumns.settl_curr_fx_rate_calc.value, MiddleOfficeColumns.total_fees.value,
             MiddleOfficeColumns.client_comm.value],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values(
            {MiddleOfficeColumns.sts.value: 'ApprovalPending', MiddleOfficeColumns.match_status.value: 'Unmatched',
             MiddleOfficeColumns.settl_currency.value: 'UAH', MiddleOfficeColumns.exchange_rate.value: '2',
             MiddleOfficeColumns.settl_curr_fx_rate_calc.value: 'M',
             MiddleOfficeColumns.total_fees.value: expected_fees,
             MiddleOfficeColumns.client_comm.value: expected_comm},
            values_after_book,
            'Comparing values after Book for block of MiddleOffice')
        # endregion

        # region Approve
        self.middle_office.approve_block()
        # endregion

        # region Extracting values from Allocation ticket
        extract_panels = self.middle_office.extracting_values_from_allocation_ticket(
            [PanelForExtraction.SETTLEMENT], {MiddleOfficeColumns.order_id.value: order_id})
        values_from_panels = {}
        for d in self.middle_office.split_tab_misk(extract_panels):
            values_from_panels.update(d)
        # endregion

        # region Comparing Exchange Rate values in Allocation ticket
        self.middle_office.compare_values(
            {MiddleOfficeColumns.settl_currency.value: 'UAH', MiddleOfficeColumns.exchange_rate.value: '2',
             'ExchangeRateCalc': 'Multiply'},
            {MiddleOfficeColumns.settl_currency.value: values_from_panels.get('SettlCurrency'),
             MiddleOfficeColumns.exchange_rate.value: values_from_panels.get('ExchangeRate'),
             'ExchangeRateCalc': values_from_panels.get('ExchangeRateCalc')},
            'Comparing Exchange Rate values in Allocation ticket')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
