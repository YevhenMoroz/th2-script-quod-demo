import random
import string
import logging
import time
from pathlib import Path
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, ExecSts, OrderBookColumns, ExecPcy
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_3874(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "900"
        self.price = "20"
        self.qty_per = "100"
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.route = self.data_set.get_route('route_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.fix_message.change_parameter("Account", "CLIENT_FIX_CARE")
        self.strat = "TWAP(ASIA)"
        self.rule_manager = RuleManager(Simulators.equity)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_co_1_venue_1")
        self.route_desk = "Route via FIXBUYTH2 - component used by TH2 simulator and autotests"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create first CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # endregion
        # region create second CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region create basket
        self.order_book.create_basket([1, 2], self.basket_name)
        # endregion
        # region get basket id
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value)
        # endregion
        # region Wave Basket
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
            self.basket_book.set_external_algo_twap_details(strategy_type=self.strat, urgency="LOW")
            self.basket_book.wave_basket(qty_percentage=self.qty_per, route=self.route)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rele)
        # endregion
        # check basket waves fields
        self.basket_book.check_basket_sub_lvl_field(1, BasketBookColumns.status_wave.value,
                                                    BasketBookColumns.waves_tab.value, ExecSts.terminated.value)
        self.basket_book.check_basket_sub_lvl_field(1, BasketBookColumns.percent_qty_to_release.value,
                                                    BasketBookColumns.waves_tab.value, self.qty_per)
        self.basket_book.check_basket_sub_lvl_field(1, BasketBookColumns.route_name.value,
                                                    BasketBookColumns.waves_tab.value, "ESBUYTH2TEST")
        # endregion
        # check basket waves fields
        order_id1 = self.order_book.set_filter([OrderBookColumns.basket_id.value, basket_id]).extract_field(OrderBookColumns.order_id.value)
        order_id2 = self.order_book.set_filter([OrderBookColumns.basket_id.value, basket_id]).extract_field(
            OrderBookColumns.order_id.value, 2)
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_second_lvl_fields_list(
            {OrderBookColumns.sts.value: ExecSts.terminated.value, OrderBookColumns.exec_sts.value: ExecSts.filled.value,
             OrderBookColumns.exec_pcy.value: ExecPcy.dma.value, OrderBookColumns.route_descr.value: self.route_desk})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_second_lvl_fields_list(
            {OrderBookColumns.sts.value: ExecSts.terminated.value,
             OrderBookColumns.exec_sts.value: ExecSts.filled.value,
             OrderBookColumns.exec_pcy.value: ExecPcy.dma.value, OrderBookColumns.route_descr.value: self.route_desk})
        # endregion
