import logging
import random
import string

from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5024"
    client = "CLIENT_FIX_CARE"

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    basket_template_name = "Test Template"
    path_xlsx = "C:\\Users\\" + "IPalamarchuk" + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                 '\\Basket_import_files\\BasketTemplate_withHeader_Mapping1.xlsx'
    path_csv = "C:\\Users\\" + "IPalamarchuk" + '\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket' \
                                                '\\Basket_import_files\\BasketTemplate_withHeader_Mapping2.csv'

    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    basket_name_2 = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))

    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create Basket via import
    eq_wrappers.create_basket_via_import(base_request, basket_name, basket_template_name, path_xlsx, client)
    eq_wrappers.create_basket_via_import(base_request, basket_name_2, basket_template_name, path_csv, client,
                                         is_csv=True)

    orders_qty = eq_wrappers.get_basket_orders_values(base_request, 2, "Qty", {'Basket Name': basket_name_2})
    eq_wrappers.base_verifier(case_id, "Qty", "300", orders_qty.get("1"))
    eq_wrappers.base_verifier(case_id, "Qty", "400", orders_qty.get("2"))
