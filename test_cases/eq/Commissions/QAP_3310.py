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
from test_framework.win_gui_wrappers.data_set import MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_3310(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "3310"
        self.price = "3310"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1

    def execute(self):
        case_id = create_event(self.__class__.__name__, self.report_id)
        main_window = BaseMainWindow(case_id, self.session_id)
        RestCommissionsSender(self.wa_connectivity, case_id).send_default_fee()
        self.__open_front_end(main_window, self.report_id)
        self.__send_fix_orders(self.client, self.price, self.qty, case_id)
        middle_office = OMSMiddleOfficeBook(case_id, self.session_id)
        order_book = OMSOrderBook(case_id, self.session_id)
        order_book.scroll_order_book(1)
        middle_office.book_order()
        middle_office.set_modify_ticket_details(remove_fee=True)
        middle_office.amend_block()
        self.__verify_fees(middle_office)

    def __open_front_end(self, main_window, report_id):
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        main_window.open_fe(report_id, work_dir, username, password)

    def __send_fix_orders(self, client, price, qty, case_id):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account.value, 'AllocQty': qty}]}
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, client + '_EUREX', "XEUR", float(price), float(price), int(qty),
                int(qty), 1)
            fix_manager = FixManager(self.ss_connectivity, case_id)
            new_order_single = FixMessageNewOrderSingleOMS().set_default_dma_limit_eurex().add_ClordId(
                (os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': qty}, "Price": price, "Account": client, 'PreAllocGrp': no_allocs})
            self.response: list = fix_manager.send_message_and_receive_response_fix_standard(new_order_single)
        finally:
            time.sleep(2)
            rule_manager.remove_rule(nos_rule)

    @staticmethod
    def __verify_fees(middle_office: OMSMiddleOfficeBook):
        fees = middle_office.extract_block_field(MiddleOfficeColumns.fees.value)
        middle_office.compare_values({MiddleOfficeColumns.fees.value: ""}, fees, event_name='Check values')
