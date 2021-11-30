import logging
import os
import string
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
import random

from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4007"
    # region Declarations
    client = "CLIENT_FIX_CARE"
    qty1 = "600"
    qty2 = "500"
    price1 = "20"
    price2 = "10"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    basket_template_name = "Test Template 2"
    path_csv = "C:\\Users\\" + username + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                          '\\Basket_import_files\\BasketTemplate_withoutHeader_Mapping1.csv'

    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create Basket via import
    eq_wrappers.create_basket_via_import(base_request, basket_name, basket_template_name, path_csv, client, is_csv=True)
    # endregion
    # region Manual Execute orders
    orders_id = eq_wrappers.get_basket_orders_values(base_request, 2, "Id", {'Basket Name': basket_name})
    eq_wrappers.verify_order_value(base_request, case_id, "Basket Name", basket_name,
                                   order_filter_list=["Order ID", orders_id["1"]])
    eq_wrappers.manual_execution(base_request, qty1, price1)
    eq_wrappers.verify_order_value(base_request, case_id, "Basket Name", basket_name,
                                   order_filter_list=["Order ID", orders_id["2"]])
    eq_wrappers.manual_execution(base_request, qty2, price2)
    # endregion
    # region Complete Book
    eq_wrappers.complete_basket(base_request)
    # endregion
    # region Book Basket
    eq_wrappers.book_basket(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "Booked",
                                   order_filter_list=["Order ID", orders_id["1"]])
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "Booked",
                                   order_filter_list=["Order ID", orders_id["2"]])
    # endregion

