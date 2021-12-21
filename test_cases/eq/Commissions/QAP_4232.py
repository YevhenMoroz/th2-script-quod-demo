import logging
import os
import time

from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import CommissionClients, CommissionAccounts
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.data_set import TradeBookColumns, MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_4232(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "4232"
        self.price = "4232"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1
        self.case_id = create_event(self.__class__.__name__, self.report_id)

    def execute(self):
        main_window = BaseMainWindow(self.case_id, self.session_id)
        trades = OMSTradesBook(self.case_id, self.session_id)
        commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id)
        middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        commission_sender.clear_fees()
        commission_sender.modify_fees_request(recalculate=True).change_params({"venueID": "EUREX"}).send_post_request()
        self.__open_front_end(main_window, self.report_id)
        self.__send_fix_orders()
        self.__verify_fees_of_executions(trades)
        middle_office.set_modify_ticket_details(remove_fee=True)
        middle_office.book_order()
        self.__verify_fees_in_middle_office(middle_office)
        middle_office.approve_block()
        middle_office.allocate_block()
        self.__verify_fees_in_allocation_ticket(middle_office)

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account.value, 'AllocQty': self.qty}]}
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, self.client + '_EUREX', "XEUR", float(self.price), float(self.price),
                int(self.qty), int(self.qty), 1)
            fix_manager = FixManager(self.ss_connectivity, self.case_id)
            new_order_single = FixMessageNewOrderSingleOMS().set_default_dma_limit_eurex().add_ClordId(
                (os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 'PreAllocGrp': no_allocs})
            self.response: list = fix_manager.send_message_and_receive_response_fix_standard(new_order_single)
        finally:
            time.sleep(2)
            rule_manager.remove_rule(nos_rule)

    @staticmethod
    def __open_front_end(main_window, report_id):
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        main_window.open_fe(report_id, work_dir, username, password)

    def __verify_fees_of_executions(self, trades: OMSTradesBook):
        order_id = self.response[0].get_parameter("OrderID")
        trades.set_filter(["Order ID", order_id])
        fees = {TradeBookColumns.exec_fees.value: trades.extract_field(TradeBookColumns.exec_fees.value)}
        trades.compare_values({TradeBookColumns.exec_fees.value: ""}, fees, event_name='Check values')

    @staticmethod
    def __verify_fees_in_middle_office(middle_office: OMSMiddleOfficeBook):
        fees = middle_office.extract_block_field(MiddleOfficeColumns.fees.value)
        middle_office.compare_values({MiddleOfficeColumns.fees.value: ""}, fees, event_name='Check values')

    @staticmethod
    def __verify_fees_in_allocation_ticket(middle_office: OMSMiddleOfficeBook):
        fees = middle_office.extract_allocate_value(AllocationsColumns.fees.value)
        middle_office.compare_values({AllocationsColumns.fees.value: "1.123"}, fees, event_name='Check values')
