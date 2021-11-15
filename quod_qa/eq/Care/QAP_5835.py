import logging
import os

from custom.basic_custom_actions import create_event
from quod_qa.win_gui_wrappers.base_window import BaseWindow
from quod_qa.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from quod_qa.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5835"
    case_id = create_event(case_name, report_id)
    # region Declarations
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    base_window = BaseWindow(case_id, session_id)
    oms_order_book = OMSOrderBook(case_id, session_id)
    base_window.open_fe(session_id, report_id, work_dir, username, password)
    # endregion
    fix_manager = FixManager('fix-sell-317-standard-test', case_id)
    fix_message_new_order_single = FixMessageNewOrderSingleOMS()
    fix_message_new_order_single.set_default_DMA()
    fix_message_new_order_single.change_parameters({"HandlInst": "3", "Account": "MOClient3_PARIS"})
    fix_manager.send_message(fix_message_new_order_single)
    oms_order_book.scroll_order_book(1)
    client = oms_order_book.extract_field('Client ID')
    actually_dict = {'Client ID': client}
    base_window.compare_values({'Client ID': 'MOClient2'}, actually_dict, 'Compare Client ID')
