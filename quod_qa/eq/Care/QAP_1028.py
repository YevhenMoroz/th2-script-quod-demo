import logging
from th2_grpc_hand import rhbatch_pb2
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event
from stubs import Stubs
from win_gui_modules.utils import get_base_request


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1028"
    # region Declarations
    qty = "900"
    price = "40"
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
    desk = "Desk of Dealers 3 (CL)"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    base_request2 = get_base_request(session_id2, case_id)

    # endregion
    # region open FE
    eq_wrappers.open_fe(session_id,report_id,case_id,work_dir,username,password)
    eq_wrappers.open_fe2(session_id2,report_id,work_dir,username2,password2)
    # endregion
    # region switch user 1
    eq_wrappers.switch_user(session_id, case_id)
    # endregion
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, "Limit", is_care=True, recipient=username2, price=price)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    # region switch user 2
    eq_wrappers.switch_user(session_id2, case_id)
    # endregion
    # region Reassign order
    eq_wrappers.reassign_order(base_request2, desk)
    # endregion
    eq_wrappers.verify_order_value(base_request2, case_id, "Sts", "Sent")
    # region switch user 1
    eq_wrappers.switch_user(session_id, case_id)
    # endregion
    # region Reject order
    eq_wrappers.reject_order(lookup, qty, price)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")

