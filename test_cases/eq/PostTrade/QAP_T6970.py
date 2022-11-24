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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns, PostTradeStatuses, ExecSts
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6970(TestCase):
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
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
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
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            cl_ord_id = response[0].get_parameters()['ClOrdID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Checking Execution report
        self.execution_report.set_default_filled(self.fix_message)
        self.execution_report.change_parameters(
            {'ReplyReceivedTime': '*', 'LastMkt': '*', 'Text': '*', 'Account': self.client})
        self.execution_report.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report, ignored_fields=['SecurityDesc'])
        # endregion

        # region Checking statuses in OrderBook
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                                 OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                                 OrderBookColumns.done_for_day.value: 'Yes'},
                                                'Comparing statuses after trading')
        # endregion

        # region Book order
        self.middle_office.set_modify_ticket_details(settl_currency='UAH', exchange_rate='0,222',
                                                     exchange_rate_calc='Divide')
        self.middle_office.book_order([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        # endregion

        # region Extracting values from Booking ticket
        extract_settlement_tab_booking = self.middle_office.extracting_values_from_amend_ticket(
            [PanelForExtraction.SETTLEMENT])
        fields_for_dlt = ('SettlAmount', 'SettlDate', 'PSET', 'PSETBIC')
        expected_book_ticket_values = {}
        for d in self.middle_office.split_tab_misk(extract_settlement_tab_booking):
            expected_book_ticket_values.update(d)
            for key in fields_for_dlt:
                expected_book_ticket_values.pop(key, None)
        # endregion

        # region Comparing values in Booking ticket
        self.middle_office.compare_values(
            {MiddleOfficeColumns.settl_currency.value: 'UAH', MiddleOfficeColumns.exchange_rate.value: '0.222',
             'ExchangeRateCalc': 'Divide'}, expected_book_ticket_values, 'Comparing values in Booking ticket')
        # endregion

        # region Approve and Allocate block
        self.middle_office.approve_block()
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.alloc_account, AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        # endregion

        # region Extracting values from Allocations ticket
        extract_settlement_tab_alloc = self.middle_office.extract_values_from_amend_allocation_ticket(
            panels_extraction=[PanelForExtraction.SETTLEMENT])
        expected_alloc_ticket_values = {}
        for d in self.middle_office.split_tab_misk(extract_settlement_tab_alloc):
            expected_alloc_ticket_values.update(d)
            for key in fields_for_dlt:
                expected_alloc_ticket_values.pop(key, None)
        # endregion

        # region Comparing values in Allocations ticket
        self.middle_office.compare_values(
            {MiddleOfficeColumns.settl_currency.value: 'UAH', MiddleOfficeColumns.exchange_rate.value: '0.222',
             'ExchangeRateCalc': 'Divide'}, expected_alloc_ticket_values, 'Comparing values in Allocations ticket')
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
