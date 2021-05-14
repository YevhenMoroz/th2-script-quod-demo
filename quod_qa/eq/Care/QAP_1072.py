import logging
import os
from copy import deepcopy
from datetime import datetime
from th2_grpc_act_gui_quod import order_ticket_service

from custom.verifier import Verifier
from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails, CancelOrderDetails
from custom.basic_custom_actions import create_event, timestamps
import time
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_manager import FixManager
from rule_management import RuleManager
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

def execute(report_id):
    case_name = "QAP-1072"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    newQty = "100"
    price = "40"
    newPrice = "1"
    time = datetime.utcnow().isoformat()
    lookup = "PROL"
    client = "CLIENTSKYLPTOR"
    # endregion
    list_param = {'qty': qty, 'Price': newPrice}
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
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    param_list = {'Price': newPrice}
    # region ManualExecute
    eq_wrappers.manual_execution(base_request, str(int((int(qty)/2))), price)
    response = fix_message.pop('response')
    # Amend fix order
    response = eq_wrappers.amend_order_via_fix(fix_message, case_id, param_list)
    # endregion
    # region accept amend
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('LmtPrice', '1',
                            response)
    verifier.verify()


