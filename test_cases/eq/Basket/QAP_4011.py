import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, OrderBookColumns, \
    ExecSts, MenuItemFromOrderBook
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
import getpass
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_4011(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.username = getpass.getuser()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.client = self.data_set.get_client_by_name('client_pos_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.path_csv = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                          '\\Basket_import_files\\BasketTemplate_withHeader_Mapping2.csv'
        self.item_of_menu = MenuItemFromOrderBook.add_to_basket.value


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket via template csv
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_csv, client=self.client, tif=TimeInForce.DAY.value, is_csv=True)
        # endregion
        # region create first CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region manual exec order
        self.order_book.manual_execution()
        # endregion
        # region filled status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region check present of item
        result = self.order_book.is_menu_item_present("Add to Basket", [1], filter_dict={OrderBookColumns.order_id.value: order_id})
        # endregion
        print(result)
        # region check present of item
        self.order_book.compare_values({'Is item present at menu': 'false'}, {'Is item present at menu': result},
                                       f'Verifying, that {self.item_of_menu} '
                                       f'doesn`t present at menu item')
        # endregion


#