from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, \
    CancelOrderDetails, ExtractionAction
from stubs import Stubs
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
from custom.basic_custom_actions import timestamps, create_event
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe, get_opened_fe
import logging
from rule_management import RuleManager
from datetime import datetime
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodNOSRule, TemplateQuodOCRRRule, TemplateQuodOCRRule
from th2_grpc_common.common_pb2 import ConnectionID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    act = Stubs.win_act_order_ticket
    act2 = Stubs.win_act_order_book
    common_act = Stubs.win_act

    bs_paris = 'fix-bs-eq-paris'
    bs_trqx = 'fix-bs-eq-trqx'

    rule_manager = RuleManager()
    nos_paris = rule_manager.add_NOS(bs_paris, "CLIENT1")
    nos_trqx = rule_manager.add_NOS(bs_trqx, "CLIENT1")
    ocrr_paris = rule_manager.add_OCRR(bs_paris)
    ocrr_trqx = rule_manager.add_OCRR(bs_trqx)
    ocr_paris = rule_manager.add_OCR(bs_paris)
    ocr_trqx = rule_manager.add_OCR(bs_trqx)

    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-1987"
    # "Send Stop Limit Algo order modify price, stop price and qty multiple times"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    try:
        qty = "1300"
        limit = "20"
        stop_price = "20"
        lookup = "BP"
        # lookup = "SGOA"

        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_client('Client1')
        order_ticket.set_stop_price(stop_price)
        multilisting_strategy = order_ticket.add_multilisting_strategy("Quod MultiListing")
        multilisting_strategy.set_allow_missing_trim(True)
        multilisting_strategy.set_available_venues(True)
        order_ticket.sell()

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)

        call(act.placeOrder, new_order_details.build())

        order_info_extraction = "getOrderInfo"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["Owner", Stubs.custom_config['qf_trading_fe_user_305'], "Lookup", lookup])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_ord_type = ExtractionDetail("ordType", "OrdType")
        main_order_id = ExtractionDetail("order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_status, main_order_ord_type, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", main_order_status.name, "Open"),
                                                      verify_ent("Order OrdType", main_order_ord_type.name, "StopLimit")]))

        order_id = request[main_order_id.name]
        if not order_id:
            raise Exception("Order id is not returned")

        # 5 step check StpPx, LmtPrice and Qty

        order_amend = OrderTicketDetails()
        order_amend.set_quantity('1000')
        order_amend.set_limit('19')
        order_amend.set_stop_price('19')

        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_order_details(order_amend)
        amend_order_details.set_filter(["Order ID", order_id])

        call(act2.amendOrder, amend_order_details.build())

        order_info_extraction_amend1 = "getOrderInfoAmend1"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction_amend1)
        main_order_details.set_filter(["Order ID", order_id])

        main_order_lmt_price = ExtractionDetail("order.LmtPrice", "LmtPrice")
        main_order_stop_price = ExtractionDetail("order.StpPx", "StpPx")
        main_order_qty = ExtractionDetail("order.Qty", "Qty")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_lmt_price, main_order_stop_price, main_order_qty])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(order_info_extraction_amend1, "checking order",
                                                     [verify_ent("Order LmtPrice", main_order_lmt_price.name, "19"),
                                                      verify_ent("Order Qty", main_order_qty.name, "1,000"),
                                                      verify_ent("Order StpPx", main_order_stop_price.name, "19")]))

        # 6 step check StpPx, LmtPrice and Qty

        order_amend2 = OrderTicketDetails()
        order_amend2.set_quantity('1700')
        order_amend2.set_limit('21')
        order_amend2.set_stop_price('21')

        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_order_details(order_amend2)
        amend_order_details.set_filter(["Order ID", order_id])

        call(act2.amendOrder, amend_order_details.build())

        order_info_extraction_amend2 = "getOrderInfoAmend2"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction_amend2)
        main_order_details.set_filter(["Order ID", order_id])

        main_order_lmt_price = ExtractionDetail("order.LmtPrice", "LmtPrice")
        main_order_stop_price = ExtractionDetail("order.StpPx", "StpPx")
        main_order_qty = ExtractionDetail("order.Qty", "Qty")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_lmt_price, main_order_stop_price, main_order_qty])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(order_info_extraction_amend2, "checking order",
                                                     [verify_ent("Order LmtPrice", main_order_lmt_price.name, "21"),
                                                      verify_ent("Order Qty", main_order_qty.name, "1,700"),
                                                      verify_ent("Order StpPx", main_order_stop_price.name, "21")]))
        # 7 step check Status

        # Cancelling order

        cancel_order_details = CancelOrderDetails()
        cancel_order_details.set_default_params(base_request)
        cancel_order_details.set_filter(["Order ID", order_id])
        cancel_order_details.set_comment("Order cancelled by script")
        cancel_order_details.set_cancel_children(True)

        call(act2.cancelOrder, cancel_order_details.build())

        # Checking cancelled order status
        order_info_extraction_cancel = "getOrderInfo_cancelled"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction_cancel)
        main_order_details.set_filter(["Order ID", order_id])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_details.add_single_order_info(OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=main_order_status)))

        call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(order_info_extraction_cancel, "checking order",
                                                     [verify_ent("Order Status", main_order_status.name, "Cancelled")]))
    except Exception:
        logger.error("Error execution", exc_info=True)
    rule_manager.remove_rule(nos_paris)
    rule_manager.remove_rule(nos_trqx)
    rule_manager.remove_rule(ocrr_paris)
    rule_manager.remove_rule(ocrr_trqx)
    rule_manager.remove_rule(ocr_paris)
    rule_manager.remove_rule(ocr_trqx)

    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
