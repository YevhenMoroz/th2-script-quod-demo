import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.order_ticket import ExtractOrderTicketValuesRequest

from win_gui_modules.utils import set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = "QAP-3328"
    # region Declarations
    qty = "100"
    price = "10"
    new_price = "1"
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"

    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    fix_message.pop('response')
    fix_message1 = FixMessage(fix_message)
    # endregion
    # region Accept
    eq_wrappers.accept_order(lookup, qty, price)
    # region
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    eq_wrappers.amend_order(base_request)
    req = ExtractOrderTicketValuesRequest(base_request)
    req.get_client_state()
    req.get_instrument_state()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketValues, req.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View", result['CLIENT'],
                            "False"
                            )
    verifier.verify()
