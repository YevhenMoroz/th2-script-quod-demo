import logging
import time
import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier, VerificationMethod
from test_cases.wrapper import eq_wrappers, eq_fix_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4458"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "3"
    client = "MOClient3"
    lookup = "VETO"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # # region Create CO
    eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup,qty,price)
    # endregion
    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region check order at order book
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook')
    eq_wrappers.verify_order_value(base_request, case_id, 'DoneForDay', 'Yes')
    # endregion
    # region check middle office
    response = eq_wrappers.view_orders_for_block(base_request, 1)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order not equal to the created order", eq_wrappers.get_order_id(base_request),
                            response[0]["middleOffice.orderId"], VerificationMethod.NOT_EQUALS)
    verifier.verify()
    # endregion
