import logging
from datetime import datetime


from th2_grpc_hand import rhbatch_pb2

from quod_qa.wrapper import eq_wrappers
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-1019"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    qty = "900"
    price = "20"
    client = "CLIENT1"
    lookup = "PROL"
    order_type = "Limit"

    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    session_id = set_session_id()
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    init_event = create_event("Initialization", parent_id=report_id)
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    base_request2 = get_base_request(session_id2, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']
    desk = Stubs.custom_config['qf_trading_fe_user_desk']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    eq_wrappers.open_fe2(session_id2, report_id, work_dir, username2, password2)
    # endregion
    # region switch user 1
    eq_wrappers.switch_user(session_id, case_id)
    # endregion1
    # region Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, is_care=True, recipient=desk, price=price)
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
    # region switch to user2
    eq_wrappers.switch_user(session_id2, case_id)
    # endregion
    # region Reject CO
    eq_wrappers.reject_order(lookup, qty, price)
    # endregion
    # region Check values in OrderBook after Accept
    set_base(session_id, case_id)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                     [verify_ent("Order Status", order_status.name, "Rejected")]))
    # endregion

    close_fe(case_id, session_id2)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
