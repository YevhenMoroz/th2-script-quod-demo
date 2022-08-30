import getpass
import logging
import random
import string
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7202(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.username = getpass.getuser()
        self.bas_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_co_1")
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.basket_template_name = self.data_set.get_basket_template("template5")
        self.path = "C:\\Users\\" + self.username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                    '\\Basket_import_files\\BasketTemplate_withCustomDelimiter.csv'


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create basket
        self.bas_book.create_basket_via_import(self.basket_name, self.basket_template_name, self.path, self.client,
                                               is_csv=True)
        # endregion
        # region Check Basket book
        self.bas_book.check_basket_field(BasketBookColumns.basket_name.value, self.basket_name)
        # endregion
