from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4896"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "4"
    client = "MOClient"
    lookup = "VETO"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Execute CO
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    exec_id = eq_wrappers.get_2nd_lvl_order_detail(base_request, "ExecID")
    # endregion
    # region Cancel Exec
    eq_wrappers.cancel_execution(base_request, {'ExecID': exec_id})
    # endregion
    # region Verify exec
    eq_wrappers.verify_execution_value(base_request, case_id, "ExecType", "TradeCancel", ["ExecID", exec_id])
    # endregion
    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region Verify block
    eq_wrappers.verify_block_value(base_request, case_id, "Qty", str(int(qty) / 2))
    # endregion
