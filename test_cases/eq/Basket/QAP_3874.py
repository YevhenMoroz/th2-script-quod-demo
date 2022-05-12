import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, ExecSts
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
        self.route = self.data_set.get_route('route_2')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')


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
        self.basket_book.wave_basket(qty_percentage=self.qty_per, route=self.route)
        # endregion
        # check basket 2nd level fields
        self.basket_book.check_basket_sub_lvl_field(1,  "Status", "Waves", "New")
        self.basket_book.check_basket_sub_lvl_field(1, "Percent Qty To Release", "Waves", self.qty_per)
        self.basket_book.check_basket_sub_lvl_field(1, "Route Name", "Waves", "ESCHIX")
        # endregion
