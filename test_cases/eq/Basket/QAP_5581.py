import logging
import os
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


class QAP_5581(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        bas_book = OMSBasketOrderBook(self.case_id, self.session_id)
        client = self.data_set.get_client_by_name("client_co_1")
        username = self.fe_env.user_1
        basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        basket_template_name = self.data_set.get_basket_template("template5")
        path = os.path.abspath("test_cases/eq/Basket/Basket_import_files/BasketTemplate_withCustomDelimiter.csv")
        # endregion
        # region Create basket
        bas_book.create_basket_via_import(basket_name, basket_template_name, path, client, is_csv=True)
        # endregion
        # region Check Basket book
        act_basket_name = bas_book.get_basket_value(BasketBookColumns.basket_name.value)
        bas_book.compare_values({"basket_name": basket_name}, {"basket_name": act_basket_name}, "Compare Basket Name")
        # endregion
