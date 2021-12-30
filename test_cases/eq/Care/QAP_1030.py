import logging
from th2_grpc_hand import rhbatch_pb2

from custom.verifier import VerificationMethod
from custom.basic_custom_actions import create_event
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe, switch_user
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
    client = "CLIENT_FIX_CARE_WB"
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
    open_fe(session_id, report_id, case_id, work_dir, username)
    eq_wrappers.open_fe2(session_id2, report_id, work_dir, username2, password2)
    # endregion
    # region switch user 1
    switch_user()
    # endregion
    # region Create CO
    eq_fix_wrappers.create_order_via_fix(case_id, "3", 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region transfer order
    eq_wrappers.transfer_order(base_request, username2)
    # endregion
    # region reject transfer
    switch_user()
    eq_wrappers.internal_transfer(base_request2, False)
    # endregion
    eq_wrappers.base_verifier(case_id, 'Recpt', username, eq_wrappers.get_order_value(base_request, 'Recpt'),
                              VerificationMethod.CONTAINS)
