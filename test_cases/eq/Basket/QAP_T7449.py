import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce, SymbolSource, BasketBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7449(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.username = environment.get_list_fe_environment()[0].user_1
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.templ = "TemplateForTest"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        def_templ = self.data_set.get_basket_template("template1")

        descript = "This is a test template"
        templ_details = {'Symbol': ['1', 'FR0004186856'], 'Quantity': ['2', '0'], 'Price': ['3', '0'],
                         'Account': ['4', 'CLIENT_FIX_CARE_SA1'], 'Side': ['5', 'Buy'], 'OrdType': ['6', 'Limit'],
                         'StopPrice': ['7', '0'], 'Capacity': ['8', 'Agency']}
        client = self.data_set.get_client_by_name("client_co_1")
        tif = TimeInForce.DAY.value
        symbol_source = SymbolSource.isin.value
        self.basket_book.clone_basket_template(self.templ, templ_filter={BasketBookColumns.name.value: def_templ})
        self.basket_book.amend_basket_template(self.templ, descript, client, tif, None, symbol_source, False, None, "1",
                                               ";", "test_tab", templ_details,
                                               templ_filter={BasketBookColumns.name.value: self.templ})
        result = self.basket_book.get_basket_template_details({BasketBookColumns.name.value: self.templ},
                                                              [BasketBookColumns.name.value,
                                                               BasketBookColumns.description.value])
        self.basket_book.compare_values({BasketBookColumns.name.value: self.templ,
                                         BasketBookColumns.description.value: descript}, result,
                                        "verify template columns")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.basket_book.remove_basket_template({BasketBookColumns.name.value: self.templ})
