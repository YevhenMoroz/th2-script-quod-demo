import logging

from th2_grpc_hand import rhbatch_pb2

from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, call, get_base_request
from quod_qa.eq import eq_wrappers
from win_gui_modules.wrappers import verify_ent, verification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-1035"
    seconds, nanos = timestamps()  # Store case start time
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT1"
    lookup = "PROL"
    order_type = "Limit"
    desk = True
    recipient = Stubs.custom_config['qf_trading_fe_user']
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']
    session_id = set_session_id()
    session_id2 = Stubs.session_id = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    eq_wrappers.open_fe2(session_id2, report_id, case_id, work_dir, username2, password2)
    #  endregion
    # region switch to user1
    eq_wrappers.switch_user(session_id, case_id)
    # endregion
    # region create CO
    eq_wrappers.create_care_order(base_request,qty, client, lookup, order_type, recipient, desk)
    # endregion

    # region switch to user2
    eq_wrappers.switch_user(session_id2, case_id)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,

                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent"),
                                                  ]))

    # endregion

