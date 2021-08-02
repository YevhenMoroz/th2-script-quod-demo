import logging
from datetime import datetime

from th2_grpc_act_gui_quod import order_ticket_service

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
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1365"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
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
    # endregion

    eq_wrappers.split_limit_order(base_request, qty, 'Limit', '21')
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketErrors, extract_errors_request.build())
    print(result)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View", result['ErrorMessage'],
                            "Error - [QUOD-11605] 'Price' (21) greater than Parent's 'Price' (20)"
                            )
    verifier.verify()

