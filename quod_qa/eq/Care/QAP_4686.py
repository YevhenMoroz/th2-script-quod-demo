import logging
from datetime import datetime

from quod_qa.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
import pyautogui
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, ModifyOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4686"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "40"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create order via fix
    eq_wrappers.create_order(base_request, qty, client, lookup, 'Limit', is_care=True, recipient=username, price=price)
    order_id = eq_wrappers.get_order_id(base_request)
    print(order_id)
    # endregion
    eq_wrappers.accept_order('VETO', qty, price)
    # Cancel order via hot key
    time.sleep(3)

    pyautogui.keyDown('del')
    pyautogui.keyUp('del')

    # endregion

    # region press Enter
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Cancelled', False)
