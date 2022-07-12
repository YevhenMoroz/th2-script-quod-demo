import time
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageListStatusOMS import FixMessageListStatusOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_5587(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_connectivity = SessionAliasOMS().ja_connectivity
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.main_window = BaseMainWindow(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.message_list = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.client = self.message_list.get_parameters()["ListOrdGrp"]["NoOrders"][0]["Account"]
        self.price = self.message_list.get_parameters()["ListOrdGrp"]["NoOrders"][0]["Price"]
        self.qty = self.message_list.get_parameters()["ListOrdGrp"]["NoOrders"][0]["OrderQtyData"]["OrderQty"]
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.route = self.data_set.get_route("route_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_co_1_venue_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create basket
        self.fix_manager.send_message_fix_standard(self.message_list)
        # endregion
        # region Set-up parameters for ListStatus
        list_status = FixMessageListStatusOMS().set_default_list_status(self.message_list)
        # endregion
        # region Check ListStatus
        self.fix_verifier.check_fix_message_fix_standard(list_status)
        # endregion
        # region Accept orders
        self.cl_inbox.accept_order()
        self.cl_inbox.accept_order()
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message_list)
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message_list, 1)
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # region Send wave request
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value)
        basket_ord_id1 = self.order_book.set_filter([OrderBookColumns.basket_id.value, basket_id]).extract_field(
            OrderBookColumns.order_id.value, 1)
        basket_ord_id2 = self.order_book.set_filter([OrderBookColumns.basket_id.value, basket_id]).extract_field(
            OrderBookColumns.order_id.value, 2)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rele = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.basket_book.wave_basket(route=self.route)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rele)
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report3 = FixMessageExecutionReportOMS(self.data_set).set_default_filled_list(self.message_list)
        exec_report3.change_parameter("LastMkt", "*")
        exec_report4 = FixMessageExecutionReportOMS(self.data_set).set_default_filled_list(self.message_list, 1)
        exec_report4.change_parameter("LastMkt", "*")
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report3,
                                                         key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        self.fix_verifier.check_fix_message_fix_standard(exec_report4,
                                                         key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        # endregion
