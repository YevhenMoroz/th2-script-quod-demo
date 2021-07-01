import os

from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, ExtractionAction
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom.basic_custom_actions import timestamps, create_event, message_to_grpc, convert_to_request
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager


logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = os.path.basename(__file__)

    # Create sub-report for case
    case_id = create_event(case_name, report_id)



    qty = "2000"
    limit = 20
    lookup = "BRNL"
    ex_destination = "XPAR"
    client = "CLIENT2"


    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-trqx", ex_destination +"_"+ client, ex_destination, limit)
    ocr_rule = rule_manager.add_OrderCancelRequest('fix-bs-eq-trqx','TRQX_CLIENT2','TRQX', True)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id, work_dir)


    try:
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(str(limit))
        order_ticket.set_client(client)
        order_ticket.set_order_type("Limit")

        twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
        twap_strategy.set_start_date("Now")
        twap_strategy.set_end_date("Now", "0.2")
        twap_strategy.set_aggressivity("Passive")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)


        set_base(session_id, case_id)
        order_ticket_service = Stubs.win_act_order_ticket
        call(order_ticket_service.placeOrder, new_order_details.build())

        time.sleep(10)

        order_info_extraction = "getOrderInfo"

        common_act = Stubs.win_act
        act2 = Stubs.win_act_order_book
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        # main_order_details.set_filter(["Misc3", "test tag 5005"])

        main_order_qty = ExtractionDetail("order.Qty", "Qty")
        # main_order_field4 = ExtractionDetail("order.FOfield4", "FO field 4")
        main_order_price = ExtractionDetail("order.Price", "LmtPrice")
        main_order_exec_pcy = ExtractionDetail("order.ExecPcy", "ExecPcy")
        # main_order_display_qty = ExtractionDetail("order.DisplayQty", "DisplQty")
        main_order_order_id = ExtractionDetail("order.Id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_qty,
                                                                                                     main_order_price,
                                                                                                     # main_order_field4,
                                                                                                     main_order_exec_pcy,
                                                                                                     # main_order_display_qty,
                                                                                                     main_order_order_id])

        sub_order_id_dt = ExtractionDetail("subOrder_lvl_1.id", "Order ID")

        lvl1_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(sub_order_id_dt))
        lvl1_details = OrdersDetails.create(info=lvl1_info)

        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action, sub_order_details=lvl1_details))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order ExecPcy", main_order_exec_pcy.name,
                                                                 "Synth (Quod TWAP)"),
                                                      verify_ent("Order Price", main_order_price.name, str(limit)),
                                                      verify_ent("Order Qty", main_order_qty.name, qty)

                                                      ]))

        sub_order_id = request[sub_order_id_dt.name]

    except Exception:
        logger.error("Error execution", exc_info=True)
    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
    # close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
