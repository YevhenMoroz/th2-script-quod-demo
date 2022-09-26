import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.fe_trading_constant import PercentageProfile, BasketBookColumns, SecondLevelTabs, \
    OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7401(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send NewOrderList
        nol = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_manager.send_message_and_receive_response_fix_standard(nol)
        nol_id = nol.get_parameter("ListID")
        # endregion
        # region Accept
        lookup = self.data_set.get_lookup_by_name("lookup_1")
        qty1 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["OrderQtyData"]["OrderQty"]
        qty2 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["OrderQtyData"]["OrderQty"]
        price1 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["Price"]
        price2 = nol.get_parameter("ListOrdGrp")['NoOrders'][1]["Price"]
        self.cl_inbox.accept_order(lookup, qty1, price1)
        self.cl_inbox.accept_order(lookup, qty2, price2)
        # endregion
        # region Wave
        percent_to_release = "50"
        self.basket_book.wave_basket(percent_to_release, PercentageProfile.remaining_qty.value,
                                     self.data_set.get_route("route_1"), basket_filter={
                BasketBookColumns.cl_basket_id.value: nol_id})
        # endregion
        # region Verify wave
        percent_qty_to_release = self.basket_book.get_basket_sub_lvl_value(1,
                                                                           BasketBookColumns.percent_qty_to_release.value,
                                                                           "Waves", basket_book_filter={
                BasketBookColumns.cl_basket_id.value: nol_id})

        percent_profile = self.basket_book.get_basket_sub_lvl_value(1, BasketBookColumns.percent_profile.value,
                                                                    "Waves", basket_book_filter={
                BasketBookColumns.cl_basket_id.value: nol_id})
        self.basket_book.compare_values({"1": PercentageProfile.remaining_qty.value}, percent_profile,
                                        "check percent_profile")
        self.basket_book.compare_values({"1": percent_to_release}, percent_qty_to_release,
                                        "check percent_qty_to_release")
        # endregion
        # region Verify child orders
        basket_cl_ord1 = nol.get_parameter("ListOrdGrp")['NoOrders'][0]["ClOrdID"]
        basket_cl_ord2 = nol.get_parameter("ListOrdGrp")['NoOrders'][1]["ClOrdID"]
        act_child_qty_1 = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.qty.value], [1],
                                                              {OrderBookColumns.cl_ord_id.value: basket_cl_ord1})
        act_child_qty_2 = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.qty.value], [1],
                                                              {OrderBookColumns.cl_ord_id.value: basket_cl_ord2})
        expected_qty1 = str(int(int(qty1) * int(percent_to_release) / 100))
        expected_qty2 = str(int(int(qty2) * int(percent_to_release) / 100))
        self.order_book.compare_values({OrderBookColumns.qty.value: expected_qty1},  act_child_qty_1[0], "compare ord 1 child 1")
        self.order_book.compare_values({OrderBookColumns.qty.value: expected_qty2}, act_child_qty_2[0], "compare ord 2 child 1")
        # endregion
        # region Wave
        self.basket_book.wave_basket(percent_to_release, PercentageProfile.remaining_qty.value,
                                    self.data_set.get_route("route_1"), basket_filter={
                BasketBookColumns.cl_basket_id.value: nol_id})
        # endregion
        # region Verify child orders
        act_child_qty_1 = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.qty.value], [1],
                                                              {OrderBookColumns.cl_ord_id.value: basket_cl_ord1})
        act_child_qty_2 = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.qty.value], [1],
                                                              {OrderBookColumns.cl_ord_id.value: basket_cl_ord2})
        expected_qty1_2 = str(int((int(qty1)-int(expected_qty1)) * int(percent_to_release) / 100))
        expected_qty2_2 = str(int((int(qty2)-int(expected_qty2)) * int(percent_to_release) / 100))
        self.order_book.compare_values({OrderBookColumns.qty.value: expected_qty1_2},  act_child_qty_1[0], "compare ord 1 child 2")
        self.order_book.compare_values({OrderBookColumns.qty.value: expected_qty2_2}, act_child_qty_2[0], "compare ord 2 child 2")
        # endregion
