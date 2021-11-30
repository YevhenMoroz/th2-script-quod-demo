import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules import trades_blotter_wrappers
from win_gui_modules.order_book_wrappers import ManualExecutingDetails

from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4830"
    # region Declarations

    qty = "800"
    price = "40"
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
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # region ManualExecute
    # eq_wrappers.accept_order(lookup, qty, price)
    manual_executing_details = ManualExecutingDetails(base_request)
    executions_details = manual_executing_details.add_executions_details()
    executions_details.set_quantity(qty)
    executions_details.set_price(price)
    executions_details.set_executing_firm('ExecutingTrader')
    executions_details.set_settlement_date_offset(1)
    executions_details.set_last_capacity("Agency")
    call(Stubs.win_act_order_book.manualExecution, manual_executing_details.build())

    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled')
    exec_id = eq_wrappers.get_2nd_lvl_detail(base_request, 'ExecID')
    cancel_manual_execution_details = trades_blotter_wrappers.CancelManualExecutionDetails()
    cancel_manual_execution_details.set_default_params(base_request)
    cancel_manual_execution_details.set_filter({'ExecID': exec_id})

    trades_service = Stubs.win_act_trades
    call(trades_service.cancelManualExecution, cancel_manual_execution_details.build())
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', '')
