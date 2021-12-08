import logging
import os
import time

from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.data_set import TradeBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_5951(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "158"
        self.price = "158"
        self.client = "CLIENT_COMM_1"

    def execute(self):
        case_name = "QAP-5951"
        case_id = create_event(case_name, self.report_id)
        main_window = BaseMainWindow(case_id, self.session_id)
        middle_office = OMSMiddleOfficeBook(case_id, self.session_id)
        trades = OMSTradesBook(case_id, self.session_id)
        order_book = OMSOrderBook(case_id, self.session_id)
        RestCommissionsSender(self.wa_connectivity, case_id).clear_fees().send_default_fee()
        self.__open_front_end(main_window, self.report_id)
        self.__send_fix_orders(self.client, self.price, self.qty, case_id)
        order_book.mass_book([1, 2])
        self.__verify_fees_in_exec(trades)
        self.__verify_fees_in_middle_office(middle_office)

    def __open_front_end(self, main_window, report_id):
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        main_window.open_fe(report_id, work_dir, username, password)

    def __send_fix_orders(self, client, price, qty, case_id):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': "CLIENT_COMM_1_SA1", 'AllocQty': qty}]}
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, client + '_EUREX', "XEUR", float(price), float(price), int(qty),
                int(qty), 1)
            fix_manager = FixManager(self.ss_connectivity, case_id)
            new_order_single1 = FixMessageNewOrderSingleOMS().set_default_dma_limit_eurex(Instrument.ISI1).add_ClordId(
                (os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs})
            new_order_single2 = FixMessageNewOrderSingleOMS().set_default_dma_limit_eurex(Instrument.ISI1).add_ClordId(
                (os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, "Side": "2",
                 'PreAllocGrp': no_allocs})
            fix_manager.send_message_fix_standard(new_order_single1)
            fix_manager.send_message_fix_standard(new_order_single2)
        finally:
            time.sleep(2)
            rule_manager.remove_rule(nos_rule)

    def __verify_fees_in_exec(self, trades: OMSTradesBook):
        trades.set_filter(["Qty", self.qty, "ExecPrice", self.price])
        commissions = {
            TradeBookColumns.client_commission.value: trades.extract_field(TradeBookColumns.client_commission.value)}
        fees = {TradeBookColumns.exec_fees.value: trades.extract_field(TradeBookColumns.exec_fees.value)}
        trades.compare_values({TradeBookColumns.client_commission.value: "1.123"}, commissions,
                              event_name='Check values')
        trades.compare_values({TradeBookColumns.exec_fees.value: "1.123"}, fees, event_name='Check values')

    @staticmethod
    def __verify_fees_in_middle_office(middle_office: OMSMiddleOfficeBook):
        commissions = middle_office.extract_block_field(MiddleOfficeColumns.client_comm.value, row_number=1)
        fees = middle_office.extract_block_field(MiddleOfficeColumns.fees.value, row_number=1)
        middle_office.compare_values({MiddleOfficeColumns.client_comm.value: "1.123"}, commissions,
                                     event_name='Check values')
        middle_office.compare_values({MiddleOfficeColumns.fees.value: "1.123"}, fees, event_name='Check values')
