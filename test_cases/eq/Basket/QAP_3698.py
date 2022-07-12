import random
import string
import logging
from pathlib import Path
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns,  TimeInForce
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_3698(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.template_name = "Test Template".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.exec_pol = "Care"
        self.descr = "This is a test template"
        self.symbol = "ISIN"
        self.client = self.data_set.get_client_by_name('client_pos_1')


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket via template csv
        templ = {'Symbol': ['Symbol', 'FR0004186856'], 'Quantity': ['Quantity', '0'], 'Price': ['Price', '0'],
                 'Account': ['Account', 'CLIENT_FIX_CARE_SA1'], 'Side': ['Side', 'Buy'],
                 'OrdType': ['OrdType', 'Limit'],
                 'StopPrice': ['StopPrice', '0'], 'Capacity': ['Capacity', 'Agency']}
        self.basket_book.add_basket_template(templ_name=self.template_name, descrip=self.descr, client=self.client, symbol_source=self.symbol,
                                             tif=TimeInForce.DAY.value, templ=templ)
        # endregion
        # region check basket fields
        result = self.basket_book.get_basket_template_details({"Name":self.template_name}, ["Name"])
        self.basket_book.compare_values({"Name" : self.template_name}, result, "template is created")
        # endregion
