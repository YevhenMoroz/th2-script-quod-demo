import logging
import os
import random
import string
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, SecondLevelTabs, \
    OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7201(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Declaration
        template_name = "testTemplate"+"".join(random.choices(string.ascii_letters + string.digits, k=5))
        client = self.data_set.get_client('client_co_1')
        account_id = self.data_set.get_account_by_name('client_co_1_acc_1')
        tif = self.data_set.get_time_in_force('time_in_force_1')
        order_type = self.data_set.get_order_type('limit')
        capacity = self.data_set.get_capacity('agency')
        basket_name = 'QAP_T7201'
        # endregion
        templ = {'Price': ['3', ''], 'Side': ['5', ''], 'OrdType': ['6', ''], 'Currency': ['7', ''],
                 'Capacity': ['8', '']}
        # # region create basket template
        self.basket_book.add_basket_template(template_name, client=client,
                                             symbol_source='ISIN',
                                             data_row='1', delimiter=';', spreadsheet_tab="Sheet1", tif=tif,
                                             templ=templ)
        # # endregion
        path_xlsx = os.path.abspath("Basket_import_files\BasketTemplate_withoutHeader_Mapping2"
                                    ".xlsx")
        # region create basket
        self.basket_book.create_basket_via_import(basket_name, template_name, path_xlsx, is_csv=False, client=client)
        # endregion

        # region step 3
        expected_results = [{'1': client, '2': client}, {'1': 'Buy', '2': 'Sell'}, {'1': order_type, '2': order_type},
                            {'1': account_id, '2': account_id}, {'1': capacity, '2': capacity}, {'1': '10', '2': '5'}]
        list_of_columns = [OrderBookColumns.client_name.value, OrderBookColumns.side.value,
                           OrderBookColumns.ord_type.value, OrderBookColumns.account_id.value,
                           OrderBookColumns.capacity.value,
                           BasketBookColumns.limit_price.value]
        for column in range(len(list_of_columns)):
            response = self.basket_book.get_basket_sub_lvl_value(2, list_of_columns[column],
                                                                 SecondLevelTabs.orders_tab.value,
                                                                 {BasketBookColumns.basket_name.value: basket_name})
            self.basket_book.compare_values(expected_results[column], response, 'Comparing values')
        # endregion
