import logging
import os
import time

from datetime import datetime

from th2_grpc_act_gui_quod.order_book_pb2 import NotifyDfdDetails
from custom import basic_custom_actions as bca
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderAnalysisAction, CalcDataContentsRowSelector, \
    OrderInfo, ExtractionAction, ExtractionDetail, ModifyOrderDetails
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails

from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, check_value, \
    create_order_analysis_events_request, create_verification_request
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_4298"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "10"
    display_qty = "5"
    price = "1"
    order_type = "Limit"
    tif = "Day"
    client = "CLIENT4"
    lookup = "AFO"
    algo = "Quod MultiListing"
    # end region

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

    # region Create Algo(TWAP) order via FE according with step 1
    # order_ticket = OrderTicketDetails()
    # order_ticket.set_quantity(qty)
    # order_ticket.set_client(client)
    # order_ticket.set_order_type(order_type)
    # order_ticket.set_tif(tif)
    # order_ticket.set_limit(price)
    # order_ticket.set_display_qty(display_qty)
    # order_ticket.sell()
    #
    # multilisting_strategy = order_ticket.add_multilisting_strategy(algo)
    # multilisting_strategy.set_allow_missing_prim(True)
    # multilisting_strategy.set_available_venues(True)
    # multilisting_strategy.set_post_mode("Single")
    #
    # new_order_details = NewOrderDetails()
    # new_order_details.set_lookup_instr(lookup)
    # new_order_details.set_order_details(order_ticket)
    # new_order_details.set_default_params(base_request)
    #
    # call(order_ticket_service.placeOrder, new_order_details.build())
    # end region

    # region extract parent OrderDetails
    extraction_id = "ParentOrderDetails"

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(extraction_id)

    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_id])
    main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))
    request = call(order_book_service.getOrdersDetails, main_order_details.request())

    order_id = request[main_order_id.name]
    # end region

    # region modify Parent order
    # order_amend = OrderTicketDetails()
    # order_amend.set_display_qty("7")
    # amend_order_details = ModifyOrderDetails()
    # amend_order_details.set_default_params(base_request)
    # amend_order_details.set_order_details(order_amend)
    #
    # call(order_book_service.amendOrder, amend_order_details.build())
    # end region

    # region extract Child OrderDetails
    child_order_info_extraction = "getOrderInfoChild"
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(child_order_info_extraction)

    child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
    child1_order_qty = ExtractionDetail("subOrder_lvl_1.Qty", "Qty")
    sub_lvl1_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child1_id, child1_order_qty])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action])
    sub_order_details_level1 = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_order_details_level1))

    call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details.request())
    # end region
    call(common_act.verifyEntities, verification(child_order_info_extraction, "checking Child order",
                                                 [verify_ent("Child Order Qty - 1", child1_order_qty.name, "1,500")]))

    # region extract Child level 2
    child_order_info_extraction1 = "getOrderInfoChild1"
    child_main_order_details_2 = OrdersDetails()
    child_main_order_details_2.set_default_params(base_request)
    child_main_order_details_2.set_extraction_id(child_order_info_extraction1)

    child2_id = ExtractionDetail("subOrder_lvl_2.id", "Order ID")
    child2_order_qty = ExtractionDetail("subOrder_lvl_2.Qty", "Qty")
    sub_lvl2_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child2_id, child2_order_qty])
    sub_lv2_1_info = OrderInfo.create(actions=[sub_lvl2_1_ext_action])
    sub_order_details_level2 = OrdersDetails.create(order_info_list=[sub_lv2_1_info])
    child_main_order_details_2.add_single_order_info(OrderInfo.create(sub_order_details=sub_order_details_level2))
    call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details_2.request())
    # region verify Child details

    call(common_act.verifyEntities, verification(child_order_info_extraction1, "checking Child order",
                                                 [verify_ent("Child Order Qty - 1", child1_order_qty.name, "1,500")]))
    # end region

    # region extract OrderAnalysisEvents
    extraction_id = "OrderAnalysisEvents"
    call(common_act.getOrderAnalysisEvents,
         create_order_analysis_events_request(extraction_id, {"Order ID": order_id}))

    analysis_event_verifier = create_verification_request("checking order events", extraction_id, extraction_id)

    check_value(analysis_event_verifier, "Event 1 Description contains", "event1.desc",
                "New User's Synthetic Order Received",
                )

    check_value(analysis_event_verifier, "Event 2 Description contains", "event2.desc", "last trade is 100@1",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 3 Description contains", "event3.desc",
                "User's Modification Received on the Synthetic Order",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 4 Description contains", "event4.desc",
                "User's Cancellation Received on the Synthetic Order",
                VerificationDetails.VerificationMethod.CONTAINS)

    call(common_act.verifyEntities, analysis_event_verifier)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
