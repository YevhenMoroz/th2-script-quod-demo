import logging
import os
import string
from returns.result import safe

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
import random
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4220"
    # region Declarations
    client = "CLIENT_FIX_CARE"
    new_qty = "900"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    basket_template_name = "Test Template"
    path_xlsx = "C:\\Users\\" + username + '\\PycharmProjects\\th2-script-quod-demo\\quod_qa\\eq\\Basket' \
                                           '\\Basket_import_files\\BasketTemplate_withHeader_Mapping1.xlsx'

    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create Basket via import
    eq_wrappers.create_basket_via_import(base_request, basket_name, basket_template_name, path_xlsx, client)

    # endregion
    # region Verify
    basket_id = eq_wrappers.get_basket_value(base_request, 'Id', {'Basket Name': basket_name})
    eq_wrappers.complete_basket(base_request, {'Id': basket_id})
    orders_id = eq_wrappers.get_basket_orders_values(base_request, 2, "Id", {'Basket Name': basket_name})

    # region verify orders
    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", 'Yes',
                                     order_filter_list=["Order ID", orders_id["2"]])
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", 'ReadyToBook')

    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", 'Yes',
                                   order_filter_list=["Order ID", orders_id["1"]])
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", 'ReadyToBook')

    eq_wrappers.verify_basket_value(base_request, case_id, "Basket Name", basket_name, {'Basket Name': basket_name})

    eq_wrappers.un_complete(base_request, {'Id': basket_id[1]})

    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", '',
                                   order_filter_list=["Order ID", orders_id["2"]])
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", '')

    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", '',
                                   order_filter_list=["Order ID", orders_id["1"]])
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", '')

    # endregion