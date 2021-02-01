import logging
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodNOSRule
from stubs import Stubs
from custom.basic_custom_actions import timestamps, create_event
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, \
    OrderInfo, OrdersDetails
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, close_fe_2
from win_gui_modules.wrappers import verification, verify_ent, set_base, order_analysis_algo_parameters_request
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

simulator = Stubs.simulator
core = Stubs.core
# conn = ConnectionID(session_alias='fix-bs-eq-trqx')
#
# NOS = simulator.createQuodNOSRule(request=TemplateQuodNOSRule(connection_id=conn))
# logger.info(f"Start rule with id: \n {NOS}")


# try:

def execute(report_id):
    act = Stubs.win_act_order_ticket
    act2 = Stubs.win_act_order_book
    common_act = Stubs.win_act
    seconds, nanos = timestamps()  # Store case start time

    case_name = "QAP-2864"
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    qty = "200"
    limit = "1"
    lookup = "CH0012268360_CHF"

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
    call(act.placeOrder, new_order_details.build())

    before_order_details_id = "beforeTWAPAlgo_order_details"
    after_order_details_id = "afterTWAPAlgo_order_details"

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(before_order_details_id)
    main_order_details.set_filter(["Owner", 'HD4'])

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

    sub_order1_qty = ExtractionDetail("subOrder1.qty", "Qty")
    sub_order2_qty = ExtractionDetail("subOrder2.qty", "Qty")
    sub_order3_qty = ExtractionDetail("subOrder3.qty", "Qty")
    sub_order4_qty = ExtractionDetail("subOrder4.qty", "Qty")

    sub_order_details = OrdersDetails()
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order1_qty)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order2_qty)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order3_qty)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order4_qty)))
    length_name = "subOrders.length"
    sub_order_details.extract_length(length_name)

    main_order_info = OrderInfo.create(sub_order_details=sub_order_details)

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(after_order_details_id)
    main_order_details.set_filter(["Order ID", order_id])
    main_order_details.add_single_order_info(main_order_info)

    call(act2.getOrdersDetails, main_order_details.request())

    call(common_act.verifyEntities, verification(after_order_details_id, "checking child orders",
                                                 [verify_ent("Sub order 1 qty", sub_order1_qty.name, "200"),
                                                  verify_ent("Sub order 2 qty", sub_order2_qty.name, "150"),
                                                  verify_ent("Sub order 3 qty", sub_order3_qty.name, "100"),
                                                  verify_ent("Sub order 4 qty", sub_order4_qty.name, "50"),
                                                  verify_ent("Sub order count", length_name, "4")]))

    extraction_id = "getOrderAnalysisAlgoParameters"

    call(common_act.getOrderAnalysisAlgoParameters,
         order_analysis_algo_parameters_request(extraction_id, ["Waves"], {"Order ID": request["order_id"]}))
    call(common_act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                 [verify_ent("Waves", "Waves", "4")]))

    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    # except Exception as e:
    #     # raise Exception()
    #     logging.error("Error execution", exc_info=True)

    # core.removeRule(NOS)
