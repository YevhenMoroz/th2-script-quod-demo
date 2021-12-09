import logging
import time

import quod_qa.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.wrappers import set_base
import pyautogui

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5979"
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT1"
    lokup = 'VETO'
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity()
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    ord_book = OMSOrderBook(case_id, session_id)
    # endregion
    # region Open FE
    ord_book.open_fe(session_id, report_id, work_dir, username, password)
    # endregion
    # region Create Order
    pyautogui.press('F5')
    pyautogui.typewrite(lokup)
    pyautogui.press('tab')
    pyautogui.typewrite(client)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.typewrite(qty)
    pyautogui.press('tab')
    pyautogui.typewrite(price)
    pyautogui.press('tab')

    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(buy_connectivity,
                                                                                         "XPAR_" + client, "XPAR",
                                                                                         float(price))
        pyautogui.press('enter')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # region Check Order Book
    sts = ord_book.extract_field("Sts")
    act_qty = ord_book.extract_field("Qty")
    ord_book.scroll_order_book()
    ord_book.compare_values({"Sts": "Open", "Qty": qty}, {"Sts": sts, "Qty": act_qty}, "Check order")
    # endregion
