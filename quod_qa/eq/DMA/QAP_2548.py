import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-2548"
    # region Declarations
    qty = "900"
    price = "30"
    client = "SBK"
    account = "Facilitation"
    lookup = "VETO"
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
    eq_wrappers.create_order(base_request, qty, client, lookup, "Limit", price=price, account=account,
                             capacity="Agency")
    eq_wrappers.verify_order_value(base_request, case_id, "Capacity", "Agency")
    eq_wrappers.verify_order_value(base_request, case_id, "ClientName", client)
    eq_wrappers.verify_order_value(base_request, case_id, "Account ID", account)
