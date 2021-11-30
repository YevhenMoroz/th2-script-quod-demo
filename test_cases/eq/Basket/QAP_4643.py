import logging
import string
import random
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4643"
    # region Declarations
    client = "CLIENT_FIX_CARE"
    qty = "900"
    price = "10"
    lookup = "VETO"
    basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create basket
    #eq_wrappers.create_basket()
    # endregion
    # region Create order
    eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Add to basket
    eq_wrappers.add_to_basket(base_request, [1], basket_name)
    # endregion
    # region Verify
    basket_id = eq_wrappers.get_basket_value(base_request, "Id", basket_name)
    eq_wrappers.verify_order_value(base_request, case_id, "Basket Name", basket_name)
    eq_wrappers.verify_order_value(base_request, case_id, "Basket ID", basket_id)
    # endregion
