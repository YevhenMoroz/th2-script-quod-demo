import logging
from datetime import datetime
from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base, direct_child_care

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# Precondition: add Recpt column
def execute(report_id):
    case_name = "QAP-1023"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "40"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    client = "CLIENTYMOROZ"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    desk = 'Desk of SalesDealers 1 (CL)'
    recipient = "HD3"
    user = "ymoroz (Yevhen Moroz)"
    # endregion

    # region open FE
    eq_wrappers.open_fe(session_id,report_id,case_id,work_dir,username,password)
    # endregion
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, "Limit", is_care=True, recipient=recipient, price=price)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    # region Reassign order
    eq_wrappers.reassign_order(base_request, desk)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")


    # region Accept order
    eq_wrappers.accept_order(lookup, qty, price)
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    eq_wrappers.verify_order_value(base_request, case_id, "Recpt", user)
    # endregion

