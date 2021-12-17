import logging
import os
import time

from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import CommissionClients, CommissionAccounts, CommissionProfiles
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.data_set import TradeBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_3350(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "3350"
        self.price = "3350"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1
        self.case_id = create_event(self.__class__.__name__, self.report_id)

    def execute(self):
        main_window = BaseMainWindow(self.case_id, self.session_id)
        trades = OMSTradesBook(self.case_id, self.session_id)
        order_book = OMSOrderBook(self.case_id, self.session_id)
        cl_inbox = OMSClientInbox(self.case_id, self.session_id)
        commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id)
        commission_sender.modify_client_commission_request(account=self.account,
                                                           comm_profile=CommissionProfiles.Abs_Amt_2
                                                           ).send_post_request()
        self.__open_front_end(main_window, self.report_id)
        self.__send_fix_orders()
        cl_inbox.accept_order("VETO", self.qty, self.price)
        order_book.manual_execution()
        self.__verify_commissions(trades)

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account.value, 'AllocQty': self.qty}]}
        fix_manager = FixManager(self.ss_connectivity, self.case_id)
        new_order_single = FixMessageNewOrderSingleOMS().set_default_care_limit_eurex().add_ClordId(
            (os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             'PreAllocGrp': no_allocs})
        self.response: list = fix_manager.send_message_and_receive_response_fix_standard(new_order_single)

    def __open_front_end(self, main_window, report_id):
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        main_window.open_fe(report_id, work_dir, username, password)

    def __verify_commissions(self, trades: OMSTradesBook):
        order_id = self.response[0].get_parameter("OrderID")
        trades.set_filter(["Order ID", order_id])
        commissions = {
            TradeBookColumns.client_commission.value: trades.extract_field(TradeBookColumns.client_commission.value)}
        trades.compare_values({TradeBookColumns.client_commission.value: "0.001"}, commissions,
                              event_name='Check values')
