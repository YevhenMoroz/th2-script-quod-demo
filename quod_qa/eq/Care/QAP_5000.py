import logging
from datetime import datetime

from th2_grpc_act_gui_quod import order_ticket_service
import time
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5000"
    # region Declarations
    qty = "40"
    price = "11"
    client = "CLIENT_FIX_CARE"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    order_id = eq_wrappers.get_order_id(base_request)
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + "_PARIS", 'XPAR', float(price))
        eq_wrappers.split_order(base_request, qty, 'Limit', price)
        order_id_child = eq_wrappers.get_2nd_lvl_detail(base_request, 'Order ID')
    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)

    # endregion
    # region check values of order

    eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Open', True)
    eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', '', False)
    # endregion
    try:
        cancel_rule = rule_manager.add_OrderCancelRequest(eq_wrappers.get_buy_connectivity(), client + "_PARIS", 'XPAR',
                                                          True)
        eq_wrappers.suspend_order(base_request, True)
    finally:
        time.sleep(5)
        rule_manager.remove_rule(cancel_rule)
    eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', 'Yes', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Cancelled', True)

