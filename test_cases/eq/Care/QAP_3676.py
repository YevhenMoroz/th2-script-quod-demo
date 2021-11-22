import test_cases.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_ticket import ExtractOrderTicketValuesRequest

from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = "QAP-3676"
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
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 1, qty, 0)
    # endregion
    # region Accept
    eq_wrappers.accept_order(lookup, qty, price)
    # region
    # region extract value
    req = ExtractOrderTicketValuesRequest(base_request)
    req.get_limit_checkbox_state()
    result = call(Stubs.win_act_order_ticket.extractOrderTicketValues, req.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View", result['LIMIT_CHECKBOX'],
                            "False"
                            )
    verifier.verify()
    # endregion