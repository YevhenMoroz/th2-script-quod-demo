import logging
import random
import string

from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4359"
    client = "CLIENT_FIX_CARE"
    basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    basket_template_name = "Test Template"
    path_to_basket = "C:\\Users\\IPalamarchuk\\PycharmProjects\\th2-script-quod-demo\\test_cases\\eq\\Basket\\Basket_import_files\\BasketTemplate_withHeader_Mapping2.csv"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    open_fe(case_id, report_id, session_id)
    eq_wrappers.create_basket_via_import(base_request, basket_name, basket_template_name, path_to_basket, client,
                                         is_csv=True)
    expected_value = 'false'
    printed_name = "Add to Basket button presence"
    verifier = Verifier(case_id)
    verifier.set_event_name("Check: " + printed_name)
    actual_value = eq_wrappers.is_menu_item_present(base_request, "Add to Basket")
    verifier.compare_values(printed_name, expected_value, actual_value['isMenuItemPresent'])
    verifier.verify()


def open_fe(case_id, report_id, session_id):
    work_dir = Stubs.custom_config['qf_trading_fe_folder_1']
    username = Stubs.custom_config['qf_trading_fe_user_1']
    password = Stubs.custom_config['qf_trading_fe_password_1']
    open_fe(session_id, report_id, case_id, work_dir, username)
