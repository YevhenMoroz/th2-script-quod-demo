import logging
import time

from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.data_set import AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_4256(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "500"
        self.price = "500"
        self.client = "MOClient"
        self.account1 = "MOClient_SA1"
        self.account2 = "MOClient_SA2"

    def execute(self):
        case_id = create_event(self.__class__.__name__, self.report_id)
        main_window = BaseMainWindow(case_id, self.session_id)
        middle_office = OMSMiddleOfficeBook(case_id, self.session_id)
        order_ticket = OMSOrderTicket(case_id, self.session_id)
        self.__open_front_end(main_window, self.report_id)
        alloc_details = {self.account1: "250", self.account2: "250"}
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, self.client + '_PARIS', "XPAR", float(self.price), float(self.price),
                int(self.qty),
                int(self.qty), 1)
            order_ticket.set_order_details(self.client, self.price, qty=self.qty, account=self.account1)
            order_ticket.create_order("VETO")
            middle_office.book_order()
            middle_office.approve_block()
            middle_office.allocate_block()
            expected_value1 = middle_office.extract_allocate_value(AllocationsColumns.qty.value)
            middle_office.compare_values({AllocationsColumns.qty.value: self.qty}, expected_value1,
                                         event_name='Compare qty')
            order_ticket.set_order_details(self.client, self.price, qty=self.qty, alloc_details=alloc_details)
            order_ticket.create_order("VETO")
            middle_office.book_order()
            middle_office.approve_block()
            middle_office.allocate_block()
            expected_value2 = middle_office.extract_allocate_value(AllocationsColumns.qty.value, account=self.account1)
            middle_office.compare_values({AllocationsColumns.qty.value: "250"}, expected_value2,
                                         event_name='Compare qty')
            expected_value3 = middle_office.extract_allocate_value(AllocationsColumns.qty.value, account=self.account2)
            middle_office.compare_values({AllocationsColumns.qty.value: "250"}, expected_value3,
                                         event_name='Compare qty')
        finally:
            time.sleep(2)
            rule_manager.remove_rule(nos_rule)

    def __open_front_end(self, main_window, report_id):
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        main_window.open_fe(report_id, work_dir, username, password)
