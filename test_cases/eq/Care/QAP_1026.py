import logging
from th2_grpc_hand import rhbatch_pb2
from custom.verifier import Verifier
from custom.basic_custom_actions import create_event
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.win_gui_wrappers.base_main_window import open_fe, switch_user
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, close_fe, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1026"

    # region Declarations
    qty = "900"
    price = "40"
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
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
    eq_wrappers.create_order(base_request, qty, client, lookup, "Limit", is_care=True, recipient=username2, price=price,
                             recipient_user=True)
    # endregion
    # region Verify
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    # endregion
    # region switch user 2
    switch_user()
    # endregion
    # region Accept
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Split
    eq_wrappers.split_limit_order(base_request2, qty, "Limit", price, "1")
    # endregion
    # region Verify
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id("getOrderInfo")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(
        extraction_details=[main_order_id])
    child_displ_qty = ExtractionDetail("lvl_1.displ_qty", "DisplQty")
    child_exec_pcy =ExtractionDetail("lvl_1.exec_pcy", "ExecPcy")
    sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
        extraction_details=[child_displ_qty,child_exec_pcy])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    main_order_details.add_single_order_info(
        OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
    request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking child Algo")
    verifier.compare_values("DisplQty", "1", request["lvl_1.displ_qty"])
    verifier.compare_values("ExecPcy", "Synth (Quod Synthetic Iceberg)", request["lvl_1.exec_pcy"])
    verifier.verify()
    # endregion
    close_fe(case_id, session_id2)
