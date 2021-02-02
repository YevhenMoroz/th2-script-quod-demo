from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, \
    ExtractionDetail, ExtractionAction
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom.basic_custom_actions import timestamps, create_event
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe_2, call, close_fe_2


logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-1641"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    qty = "8000"
    limit = "1.2"
    lookup = "NPK"
    # lookup = "PROL"

    try:
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_client("CLIENT1")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order(Stubs.custom_config['qf_trading_fe_user'], True)

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)

        set_base(session_id, case_id)

        order_ticket_service = Stubs.win_act_order_ticket
        order_book_service = Stubs.win_act_order_book
        common_act = Stubs.win_act

        call(order_ticket_service.placeOrder, new_order_details.build())

        extraction_id = "order.care"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["Lookup", lookup])

        call(order_book_service.getOrdersDetails, main_order_details.request())

        order_ticket = OrderTicketDetails()
        twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
        twap_strategy.set_start_date("Now")
        twap_strategy.set_end_date("Now", "0.5")
        twap_strategy.set_waves("4")
        twap_strategy.set_max_participation("25")
        twap_strategy.set_aggressivity("Aggressive")

        order_info_extraction = "getOrderInfo"

        call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Open")]))

        modify_order_details = ModifyOrderDetails()
        modify_order_details.set_default_params(base_request)
        modify_order_details.set_order_details(order_ticket)

        call(order_book_service.splitOrder, modify_order_details.build())

        # step 4 make trade 10000

        order_ticket_dma1 = OrderTicketDetails()
        order_ticket_dma1.set_quantity('10000')
        order_ticket_dma1.set_limit('1.2')
        order_ticket_dma1.buy()

        dma_order_details = NewOrderDetails()
        dma_order_details.set_lookup_instr(lookup)
        dma_order_details.set_order_details(order_ticket_dma1)
        dma_order_details.set_default_params(base_request)

        call(order_ticket_service.placeOrder, dma_order_details.build())

        order_ticket_dma2 = OrderTicketDetails()
        order_ticket_dma2.set_quantity('10000')
        order_ticket_dma2.set_limit('1.2')
        order_ticket_dma2.sell()

        dma_order_details = NewOrderDetails()
        dma_order_details.set_lookup_instr(lookup)
        dma_order_details.set_order_details(order_ticket_dma2)
        dma_order_details.set_default_params(base_request)

        call(order_ticket_service.placeOrder, dma_order_details.build())

        time.sleep(120)

        #  make trade 5000

        order_ticket_dma1 = OrderTicketDetails()
        order_ticket_dma1.set_quantity('5000')
        order_ticket_dma1.set_limit('1.2')
        order_ticket_dma1.buy()

        dma_order_details = NewOrderDetails()
        dma_order_details.set_lookup_instr(lookup)
        dma_order_details.set_order_details(order_ticket_dma1)
        dma_order_details.set_default_params(base_request)

        call(order_ticket_service.placeOrder, dma_order_details.build())

        order_ticket_dma2 = OrderTicketDetails()
        order_ticket_dma2.set_quantity('5000')
        order_ticket_dma2.set_limit('1.2')
        order_ticket_dma2.sell()

        dma_order_details = NewOrderDetails()
        dma_order_details.set_lookup_instr(lookup)
        dma_order_details.set_order_details(order_ticket_dma2)
        dma_order_details.set_default_params(base_request)

        call(order_ticket_service.placeOrder, dma_order_details.build())

        time.sleep(30)

        # check child orders

        extraction_id = "order.care"

        sub_lv2_1_qty = ExtractionDetail("subOrder_1_lv2.qty", "Qty")
        sub_lv2_2_qty = ExtractionDetail("subOrder_2_lv2.qty", "Qty")
        sub_lv2_3_qty = ExtractionDetail("subOrder_3_lv2.qty", "Qty")

        extraction_action_sub_lv2 = ExtractionAction.create_extraction_action(
            extraction_details=[sub_lv2_1_qty, sub_lv2_2_qty, sub_lv2_3_qty])

        # sub_lv2_details = OrdersDetails.create(info=OrderInfo.create(action=extraction_action_sub_lv2))
        # length_name = "subOrders_lv2.length"
        # sub_lv2_details.extract_length(length_name)

        sub_lv1_qty = ExtractionDetail("subOrder_lv1.qty", "Qty")
        extraction_action_sub_lv1 = ExtractionAction.create_extraction_action(extraction_detail=sub_lv1_qty)
        sub_lv1_info = OrderInfo.create(action=extraction_action_sub_lv1)
        # sub_lv1_info.set_sub_orders_details(sub_lv2_details)

        main_order_info = OrderInfo.create(sub_order_details=OrdersDetails.create(info=sub_lv1_info))

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["Lookup", lookup, "ExecPcy", "Care"])
        main_order_details.add_single_order_info(main_order_info)

        call(order_book_service.getOrdersDetails, main_order_details.request())

        call(common_act.verifyEntities, verification(
            extraction_id, "Checking child orders", [
                verify_ent("Sub Lvl 1 Qty", sub_lv1_qty.name, "8,000")
                # verify_ent("Sub 1 Lvl 2 Qty", sub_lv2_1_qty.name, "1,666"),
                # verify_ent("Sub 2 Lvl 2 Qty", sub_lv2_2_qty.name, "1,333"),
                # verify_ent("Sub 3 Lvl 2 Qty", sub_lv2_3_qty.name, "2,000"),
                # verify_ent("Sub order Lvl 2 count", length_name, "3")
            ]
        ))
    except Exception:
        logger.error("Error execution", exc_info=True)
    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
