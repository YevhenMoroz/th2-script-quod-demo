import logging
import random
import string
import time

from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4011"
    qty = "115"
    client = "CLIENT_FIX_CARE"
    price = 10
    side = 2
    tif = 0
    handle_inst = 3
    lookup = "VETO"
    basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    basket_template_name = "Test Template"
    path_to_basket = "C:\\Users\\IPalamarchuk\\PycharmProjects\\th2-script-quod-demo\\quod_qa\\eq\\Basket\\Basket_import_files\\BasketTemplate_withHeader_Mapping2.csv"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    open_fe(case_id, report_id, session_id)
    eq_wrappers.create_basket_via_import(base_request, basket_name, basket_template_name, path_to_basket, client,
                                         is_csv=True)
    buy_connectivity = eq_fix_wrappers.get_buy_connectivity()

    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_NewOrdSingle_Market(buy_connectivity, client, "XPAR", True, int(qty),
                                                    price)
        eq_fix_wrappers.create_order_via_fix(case_id, handle_inst, side, client, 1, qty, tif)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(rule)

    eq_wrappers.accept_order(lookup, qty, str(price))
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open", order_filter_list=['Qty', '115'])
    eq_wrappers.manual_execution(base_request, qty, str(price))
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
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
