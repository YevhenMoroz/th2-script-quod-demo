import getpass
import logging
import random
import string
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns, TimeInForce
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_4643(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.message_order = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.message_order.change_parameter("Account", self.client)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.username = getpass.getuser()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.path_csv = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                        '\\Basket_import_files\\BasketTemplate_withHeader_Mapping2.csv'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_csv, client=self.client, tif=TimeInForce.DAY.value,
                                                  is_csv=True)
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value)
        # endregion
        # region create CO
        self.fix_manager.send_message(self.message_order)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region add order to basket
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).add_to_basket([1], self.basket_name)
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.basket_name.value: self.basket_name, OrderBookColumns.basket_id.value: basket_id})
        # endregion