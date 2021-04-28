import logging
from datetime import datetime

from th2_grpc_hand import rhbatch_pb2

from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper.eq_wrappers import *
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, call, get_base_request
from quod_qa.wrapper import eq_wrappers
from win_gui_modules.wrappers import verify_ent, verification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-1052"
    seconds, nanos = timestamps()  # Store case start time
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    new_qty="950"
    price = "20"
    client = "CLIENT1"
    lookup = "VETO"
    order_type = "Limit"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']
    username3 = Stubs.custom_config['qf_trading_fe_user3']
    password3 = Stubs.custom_config['qf_trading_fe_password3']
    desk = Stubs.custom_config['qf_trading_fe_user_desk']
    session_id = set_session_id()
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    base_request = get_base_request(session_id, case_id)
    base_request2 = get_base_request(session_id2, case_id)
    base_request3 = get_base_request(session_id2, case_id)
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    #eq_wrappers.open_fe2(session_id2, report_id, work_dir, username2, password2)
    #  endregion
    '''
    # region switch to user1
    eq_wrappers.switch_user(session_id, case_id)
    # endregion
    # region create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type,is_care=True,resipient=desk,price=price)
    # endregion
    '''
    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")
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
    '''
    # region switch to user2
    eq_wrappers.switch_user(session_id2, case_id)
    # endregion
    # region accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    '''
    # region transfer CO
    eq_wrappers.transfer_order(base_request,username3)
    # endregion
    # region open FE
    session_id3 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    eq_wrappers.open_fe2(session_id3, report_id, work_dir, username3, password3)
    # endregion
    # region switch user
    eq_wrappers.switch_user(session_id3,case_id)
    # endregion
    # region Accept order
    eq_wrappers.accept_order(lookup,qty,price)
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")