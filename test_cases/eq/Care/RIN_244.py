import logging

from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps


from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo

from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from test_cases.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "RIN_244"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "100"
    client = "HAKKIM"
    lookup = "TCS"
    order_type = "Limit"
    tif = "Day"
    price = "30"
    recipient = "RIN-DESK (CL)"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # end region

    # region Create Care order via FE
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, True, recipient, price, False,
                             DiscloseFlagEnum.DEFAULT_VALUE)
    # end region

    order_id = eq_wrappers.get_order_id(base_request)

    # region accept order
    eq_wrappers.accept_order(lookup, qty, price)
    # end region

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_details.set_filter(["Order ID", order_id])

    order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(order_book_service.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open")]))

    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

