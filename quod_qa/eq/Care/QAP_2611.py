import logging
from datetime import datetime
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event
from stubs import Stubs

from win_gui_modules.utils import set_session_id, get_base_request


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2611"
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "YMOROZ"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    order_type = "Limit"
    washbook = "CareWB"
    account = "YM_client_SA1"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=username,
                             price=price, washbook=washbook,account=account)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, "Wash Book", "CareWB")