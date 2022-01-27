import logging
import random
import string
from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
# region TestData
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']
route = 'Route via FIXBUYTH2 - component'
ss_connectivity = SessionAliasOMS().ss_connectivity
bs_connectivity = SessionAliasOMS().bs_connectivity
path_xlsx = str(Path("test_cases/eq/Basket/Basket_import_files/BasketTemplate_withHeader_multilisting.xlsx").absolute())


# endregion

class QAP_6386(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        base_window = BaseMainWindow(self.test_id, self.session_id)
        # endregion
        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion
        # region Create Basket via Import
        basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        basket_book.create_basket_via_import(basket_name, "TemplateWithCurrencyAndVanue", path_xlsx, "CLIENT_FIX_CARE")
        # endregion
        # region Verify basket
        ord_curr = basket_book.get_basket_orders_value(2, "Venue", {"Basket Name": basket_name})
        basket_book.compare_values({"1": "CHI-X EUROPE LIMITED", "2": "Turquoise STOCK EXCHANGE"}, ord_curr,
                                   "Compare basket venue")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        pass
