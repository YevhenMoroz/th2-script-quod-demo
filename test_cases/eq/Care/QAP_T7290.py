import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Suspended, ChildOrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_child_order_book import OMSChildOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import set_session_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7290(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.session_id2 = set_session_id(self.fe_env.target_server_win)
        self.fun_config = self.fe_env.folder + "\ConfigFiles\Default\\functional.config"
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id2)
        self.child_order_book = OMSChildOrderBook(self.test_id, self.session_id2)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id2)
        self.base_main_window = BaseMainWindow(self.test_id, self.session_id2)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id2)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.venue_client = self.data_set.get_venue_client_names_by_name("client_co_1_venue_1")
        self.client = self.data_set.get_client('client_co_1')  # MOClient
        self.qty = "100"
        self.price = "10"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        tree = ET.parse(self.fun_config)
        root = tree.getroot()
        root.find("tradingOptions/orderSuspendOrRelease").set("enable", "true")
        tree.write(self.fun_config)
        self.base_main_window.open_fe(self.report_id, self.fe_env, 2, False)
        # endregion
        # region Step1
        self.fix_message.change_parameters(
            {'Account': self.client, 'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)
        # endregion
        # region Step 2,3,4,5
        try:
            rule_manager = RuleManager(sim=Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.venue_client,
                                                                                             self.mic,
                                                                                             float(self.price))

            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       self.venue_client, self.mic,
                                                                                       float(self.price),
                                                                                       int(self.qty), 60000)
            self.order_ticket.split_order(filter_list=filter_list)
            self.order_book.suspend_order(filter_dict=filter_dict)
            self.order_book.check_order_fields_list({OrderBookColumns.suspend.value: Suspended.yes.value})
        finally:
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(nos_rule)
            filter_dict = {ChildOrderBookColumns.parent_ord_id.value: order_id}
        self.child_order_book.get_child_order_value(OrderBookColumns.exec_sts.value, filter_dict)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.base_main_window.close_fe()
        tree = ET.parse(self.fun_config)
        root = tree.getroot()
        root.find("tradingOptions/orderSuspendOrRelease").set("enable", "false")
        tree.write(self.fun_config)
