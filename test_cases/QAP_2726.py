from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.application_wrappers import CloseApplicationRequest, OpenApplicationRequest, LoginDetailsRequest
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
import logging
from custom.basic_custom_actions import timestamps, create_event
from win_gui_modules.utils import set_session_id, call, get_base_request, prepare_fe_2, close_fe_2
from stubs import Stubs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-2726"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    qty = "200"
    limit = "1"
    lookup = "ADW"

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(limit)
    order_ticket.set_client("Client1")
    twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
    twap_strategy.set_start_date("Now")
    twap_strategy.set_end_date("Now", "0.5")
    twap_strategy.set_waves("10")
    twap_strategy.set_aggressivity("Aggressive")

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    set_base(session_id, case_id)

    act = Stubs.win_act_order_ticket
    act2 = Stubs.win_act_order_book
    common_act = Stubs.win_act

    call(act.placeOrder, new_order_details.build())

    before_order_details_id = "beforeTWAPAlgo_order_details"
    after_order_details_id = "afterTWAPAlgo_order_details"

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(before_order_details_id)
    main_order_details.set_filter(["Owner", Stubs.custom_config['qf_trading_fe_user']])

    main_order_status = ExtractionDetail("order_status", "Sts")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status,
                                                                                                 main_order_id])
    main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

    request = call(act2.getOrdersDetails, main_order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", main_order_status.name, "Open")]))

    order_id = request[main_order_id.name]
    if not order_id:
        raise Exception("Order id is not returned")

    time.sleep(300)

    sub_order1_exec_pcy = ExtractionDetail("subOrder1.ExecPcy", "ExecPcy")
    sub_order2_exec_pcy = ExtractionDetail("subOrder2.ExecPcy", "ExecPcy")
    sub_order3_exec_pcy = ExtractionDetail("subOrder3.ExecPcy", "ExecPcy")
    sub_order4_exec_pcy = ExtractionDetail("subOrder4.ExecPcy", "ExecPcy")

    sub_order_details = OrdersDetails()
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order1_exec_pcy)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order2_exec_pcy)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order3_exec_pcy)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order4_exec_pcy)))
    length_name = "subOrders.length"
    sub_order_details.extract_length(length_name)

    main_order_info = OrderInfo.create(sub_order_details=sub_order_details)

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(after_order_details_id)
    main_order_details.set_filter(["Order ID", order_id, "ExecPcy", "Synth (Quod TWAP)"])
    main_order_details.add_single_order_info(main_order_info)

    call(act2.getOrdersDetails, main_order_details.request())

    call(common_act.verifyEntities, verification(after_order_details_id, "checking child orders",
                                                 [verify_ent("Sub order 1 ExecPcy", sub_order1_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order 2 ExecPcy", sub_order2_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order 3 ExecPcy", sub_order3_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order 4 ExecPcy", sub_order4_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order count", length_name, "4")]))

    # step 4 Close the FrontEnd and safe workspace
    app_service = Stubs.win_act
    close_app_request = CloseApplicationRequest()
    close_app_request.set_default_params(base_request)
    close_app_request.save_workspace()
    app_service.closeApplication(close_app_request.build())

    # step 5 Open the FrontEnd login and check filter
    open_app_req = OpenApplicationRequest()
    open_app_req.set_session_id(session_id)
    open_app_req.set_parent_event_id(case_id)
    open_app_req.set_work_dir(Stubs.custom_config['qf_trading_fe_folder'])
    open_app_req.set_application_file(Stubs.custom_config['qf_trading_fe_exec'])
    app_service.openApplication(open_app_req.build())

    login_details_req = LoginDetailsRequest()
    login_details_req.set_session_id(session_id)
    login_details_req.set_parent_event_id(case_id)
    login_details_req.set_username(Stubs.custom_config['qf_trading_fe_user'])
    login_details_req.set_password(Stubs.custom_config['qf_trading_fe_password'])
    login_details_req.set_main_window_name(Stubs.custom_config['qf_trading_fe_main_win_name'])
    login_details_req.set_login_window_name(Stubs.custom_config['qf_trading_fe_login_win_name'])
    app_service.login(login_details_req.build())

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(after_order_details_id)
    main_order_details.set_filter(["Order ID", order_id])
    main_order_details.add_single_order_info(main_order_info)

    call(act2.getOrdersDetails, main_order_details.request())

    call(common_act.verifyEntities, verification(after_order_details_id, "checking child orders",
                                                 [verify_ent("Sub order 1 ExecPcy", sub_order1_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order 2 ExecPcy", sub_order2_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order 3 ExecPcy", sub_order3_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order 4 ExecPcy", sub_order4_exec_pcy.name, "DMA"),
                                                  verify_ent("Sub order count", length_name, "4")]))

    close_fe_2(case_id, session_id)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
