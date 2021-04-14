import logging
from datetime import datetime


from th2_grpc_hand import rhbatch_pb2
from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails
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
    case_name = "QAP-1022"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    qty = "900"
    new_qty = "100"
    price = "20"
    new_price = "1"
    client = "CLIENT1"
    lookup = "PROL"
    # endregion
    # region Open FE
    stub = Stubs.win_act
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    init_event = create_event("Initialization", parent_id=report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    base_request2 = get_base_request(session_id2, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    prepare_fe(init_event, session_id2, work_dir, username2, password2)
    # endregion
    # region Switch to user1
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    stub.moveToActiveFE(search_fe_req.build())
    #endregion
    # region Create CO
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT1")
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price)
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.set_care_order(Stubs.custom_config['qf_trading_fe_user'])

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    set_base(session_id, case_id)

    order_ticket_service = Stubs.win_act_order_ticket
    common_act = Stubs.win_act

    call(order_ticket_service.placeOrder, new_order_details.build())
    rule_manager.remove_rule(nos_rule)
    # endregion
    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            main_order_id,
                                                                                            order_qty,
                                                                                            order_price
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent"),
                                                  verify_ent("Qty", order_qty.name, qty),
                                                  verify_ent("LmtPrice", order_price.name, price)
                                                  ]))

    # endregion
    # region Accept CO
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Check values in OrderBook after Accept
    set_base(session_id, case_id)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open")]))
    # endregion
    # region Switch to user2
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id2)
    search_fe_req.set_parent_event_id(case_id)
    stub.moveToActiveFE(search_fe_req.build())
    set_base(session_id2, case_id)
    # endregion
    # region Amend order
    order_amend = OrderTicketDetails()
    order_amend.set_limit(new_price)
    order_amend.set_quantity(new_qty)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request2)
    amend_order_details.set_order_details(order_amend)
    call(act.amendOrder, amend_order_details.build())
    # endregion
    # region Switch to user2
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id2)
    search_fe_req.set_parent_event_id(case_id)
    stub.moveToActiveFE(search_fe_req.build())
    set_base(session_id2, case_id)
    # endregion
    # region Cancelling order
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request2)
    cancel_order_details.set_cancel_children(True)

    call(act.cancelOrder, cancel_order_details.build())
    # endregion
    # region Switch to user1
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(case_id)
    stub.moveToActiveFE(search_fe_req.build())
    set_base(session_id, case_id)
    # endregion
    # region Check values after Cancel
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled"),
                                                  verify_ent("Qty", order_qty.name, new_qty),
                                                  verify_ent("LmtPrice", order_price.name, new_price)
                                                  ]))
    # endregion

    close_fe(case_id, session_id2)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
