import logging
import os
from copy import deepcopy
from datetime import datetime

from th2_grpc_act_gui_quod import order_ticket_service

from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails, CancelOrderDetails

from custom.basic_custom_actions import create_event, timestamps
import time
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1070"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "800"
    price = "10"
    newPrice = "1"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
    # endregion
    # region Open FE

    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregionA
    # region Create CO
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    response = fix_message.pop('response')
    fix_message1 = FixMessage(fix_message)
    param_list = {'Price': newPrice}
    # Amend fix order

    eq_wrappers.amend_order_via_fix(case_id, fix_message1, param_list)
    # region

    # region AcceptOrder
    eq_wrappers.accept_modify(lookup, qty, newPrice)
    # endregion

    # region CheckOrder
    eq_wrappers.verify_order_value(base_request, case_id, 'Limit Price', '1', False)
    # endregion
