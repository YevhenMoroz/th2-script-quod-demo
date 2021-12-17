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
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_3312(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "3312"
        self.price = "3312"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1
        self.case_id = create_event(self.__class__.__name__, self.report_id)

    def execute(self):
        main_window = BaseMainWindow(self.case_id, self.session_id)
        trades = OMSTradesBook(self.case_id, self.session_id)
        commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id)
        commission_sender.clear_fees()
        commission_sender.modify_client_commission_request(account=self.account,
                                                           comm_profile=CommissionProfiles.Abs_Amt_USD
                                                           ).send_post_request()
        self.__open_front_end(main_window, self.report_id)
        self.__send_fix_orders()
        self.__verify_commissions(trades)

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
        trades.compare_values({TradeBookColumns.client_commission.value: "1.5064"}, commissions,
                              event_name='Check values')
