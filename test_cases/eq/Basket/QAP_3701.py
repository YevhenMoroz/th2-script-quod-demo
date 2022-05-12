import random
import string
import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns,  TimeInForce
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
import getpass


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_3701(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.username = getpass.getuser()
        self.client = self.data_set.get_client_by_name('client_pos_1')
        self.path_xlsx = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                               '\\Basket_import_files\\BasketTemplate_withHeader_Mapping1.xlsx'

        self.path_csv = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                              '\\Basket_import_files\\BasketTemplate_withHeader_Mapping1.csv'


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket via template csv
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_csv, client=self.client, tif=TimeInForce.DAY.value, is_csv=True)
        # endregion
        # region check basket fields
        self.basket_book.check_basket_field(BasketBookColumns.exec_policy.value, "Care")
        self.basket_book.check_basket_field(BasketBookColumns.status.value, "Executing")
        self.basket_book.check_basket_field("ListExecInstType", "Immediate")
        self.basket_book.check_basket_field(BasketBookColumns.basket_name.value, self.basket_name)
        self.basket_book.check_basket_field("TimeInForce", "DAY")
        # endregion
        # region create basket via template xlsx
        self.basket_book.create_basket_via_import(basket_name=self.basket_name,
                                                  basket_template_name="Test Template",
                                                  path=self.path_xlsx, client=self.client, tif=TimeInForce.DAY.value)
        # endregion
        # region check basket fields
        self.basket_book.check_basket_field(BasketBookColumns.exec_policy.value, "Care")
        self.basket_book.check_basket_field(BasketBookColumns.status.value, "Executing")
        self.basket_book.check_basket_field("ListExecInstType", "Immediate")
        self.basket_book.check_basket_field(BasketBookColumns.basket_name.value, self.basket_name)
        self.basket_book.check_basket_field("TimeInForce", "DAY")
        # endregion
