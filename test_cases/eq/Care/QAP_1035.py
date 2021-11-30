import logging
from th2_grpc_hand import rhbatch_pb2
from custom.basic_custom_actions import timestamps
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import *
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe, switch_user
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import call, get_base_request, close_fe
from win_gui_modules.wrappers import verify_ent, verification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id,session_id):
    case_name = "QAP-1035"
    seconds, nanos = timestamps()  # Store case start time
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    order_type = "Limit"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']
    desk = Stubs.custom_config['qf_trading_fe_user_desk']
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    eq_wrappers.open_fe2(session_id2, report_id, work_dir, username2, password2)
    #  endregion
    # region switch to user1
    switch_user()
    # endregion
    # region create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=username, price=price)
    # endregion
    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "Limit Price")
    order_pts = ExtractionDetail("order_pts", "PostTradeStatus")
    order_dfd = ExtractionDetail("order_dfd", "DoneForDay")
    order_es = ExtractionDetail("order_es", "ExecSts")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            order_pts,
                                                                                            order_dfd,
                                                                                            order_es
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent")
                                                  ]))

    # endregion
    # region switch to user2
    switch_user(session_id2, case_id)
    # endregion
    # region accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region switch to user1
    switch_user(session_id2, case_id)
    # endregion
    # region manual execution
    eq_wrappers.manual_execution(base_request, qty, price)
    # endregion
    # region complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region Check values after complete
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("Order Qty", order_qty.name, qty),
                                                  verify_ent("Order Price", order_price.name, price),
                                                  verify_ent("PostTradeStatus", order_pts.name, "ReadyToBook"),
                                                  verify_ent("DoneForDay", order_dfd.name, "Yes"),
                                                  verify_ent("ExecSts", order_es.name, "Filled")
                                                  ]))
    # endregion
    close_fe(case_id, session_id2)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
