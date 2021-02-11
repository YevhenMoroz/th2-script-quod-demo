from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, \
    ExtractionDetail, ExtractionAction
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom.basic_custom_actions import timestamps, create_event, message_to_grpc, convert_to_request
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager


logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-1641"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT1")

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    qty = "8000"
    limit = "1.2"
    lookup = "PROL"

    try:
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_client("CLIENT1")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order(Stubs.custom_config['qf_trading_fe_user_305'], True)

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

        data = call(common_act.getOrderFields, fields_request(order_info_extraction,
                                                       ["order.status", "Sts", "order.order_id", "Order ID"]))
        care_order_id = data["order.order_id"]
        # care_order_id = "CO1210211115759412001"
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Open")]))

        modify_order_details = ModifyOrderDetails()
        modify_order_details.set_default_params(base_request)
        modify_order_details.set_order_details(order_ticket)

        call(order_book_service.splitOrder, modify_order_details.build())

        # step 4 make trade 10000

        time.sleep(5)
        symbol_1 = "1042"

        MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_1,
            connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
        )).MDRefID
        mdir_params_trade = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '1.2',
                    'MDEntrySize': '10000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-eq-paris", case_id,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-eq-paris")
        ))

        time.sleep(120)

        #  make trade 5000

        mdir_params_trade_2 = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '1.2',
                    'MDEntrySize': '5000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-fh-eq-paris", case_id,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade_2, "fix-fh-eq-paris")
        ))

        time.sleep(120)

        # check child orders

        extraction_id = "child_orders"

        child_order_lvl1_details = OrdersDetails()
        child_order_lvl1_details.set_default_params(base_request)
        child_order_lvl1_details.set_extraction_id(extraction_id)
        child_order_lvl1_details.set_filter(["ParentOrdID", care_order_id])

        child_order_lvl2_1_qty = ExtractionDetail("child_order_lvl2_1.qty", "Qty")
        child_order_lvl2_1_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_lvl2_1_qty))
        child_order_lvl2_2_qty = ExtractionDetail("child_order_lvl2_2.qty", "Qty")
        child_order_lvl2_2_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_lvl2_2_qty))
        child_order_lvl2_3_qty = ExtractionDetail("child_order_lvl2_3.qty", "Qty")
        child_order_lvl2_3_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=child_order_lvl2_3_qty))

        child_order_lvl2_details = OrdersDetails.create(
            order_info_list=[child_order_lvl2_1_info, child_order_lvl2_2_info, child_order_lvl2_3_info]
        )
        length_name = "child_orders_lvl2.length"
        child_order_lvl2_details.extract_length(length_name)

        child_order_lvl1_qty = ExtractionDetail("child_order_lvl1.qty", "Qty")
        child_order_lvl1_ext_act = ExtractionAction.create_extraction_action(extraction_detail=child_order_lvl1_qty)
        child_order_lvl1_info = OrderInfo.create(
            action=child_order_lvl1_ext_act, sub_order_details=child_order_lvl2_details)

        child_order_lvl1_details.add_single_order_info(order_info=child_order_lvl1_info)

        call(order_book_service.getChildOrdersDetails, child_order_lvl1_details.request())
        call(common_act.verifyEntities, verification(
            extraction_id, "Checking child orders", [
                verify_ent("Child order lvl 1 Qty", child_order_lvl1_qty.name, "8,000"),
                verify_ent("Child order lvl 2 1 Qty", child_order_lvl2_1_qty.name, "1,666"),
                verify_ent("Child order lvl 2 2 Qty", child_order_lvl2_2_qty.name, "1,333"),
                verify_ent("Child order lvl 2 3 Qty", child_order_lvl2_3_qty.name, "2,000"),
                verify_ent("Child orders lvl 2 count", length_name, "3")
            ]
        ))
    except Exception:
        logger.error("Error execution", exc_info=True)
    rule_manager.remove_rule(nos_rule)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
