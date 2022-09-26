import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, BasketSecondLvlTabName, \
    ClientInboxColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7404(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        nol = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_manager.send_message_fix_standard(nol)
        ord_filter_1 = {ClientInboxColumns.cl_ord_id.value: nol.get_parameter('ListOrdGrp')['NoOrders'][0]['ClOrdID']}
        ord_filter_2 = {ClientInboxColumns.cl_ord_id.value: nol.get_parameter('ListOrdGrp')['NoOrders'][1]['ClOrdID']}
        self.cl_inbox.accept_order(filter=ord_filter_1)
        self.cl_inbox.accept_order(filter=ord_filter_2)
        basket_filter = {BasketBookColumns.cl_basket_id.value: nol.get_parameter("ListID")}
        self.basket_book.wave_basket(basket_filter=basket_filter)
        result = self.basket_book.is_menu_item_present(BasketBookColumns.remove_from_basket.value,
                                                       sub_lvl_tab=BasketSecondLvlTabName.orders.value,
                                                       filter_dict=basket_filter)

        self.basket_book.compare_values({"isMenuItemPresent": "false"}, {"isMenuItemPresent": result},
                                        "is 'Remove from Basket' present?")
