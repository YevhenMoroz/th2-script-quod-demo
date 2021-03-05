import logging

import rule_management as rm
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO Add another type for setQty instead Int64Value


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_order(base_request, service, qty, cur1, cur2, tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_order_book(ex_id, base_request, instr_type, act, act_ob, qty):
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_qty])))
    call(act_ob.getOrdersDetails, ob.request())
    call(act.verifyEntities, verification(ex_id, "checking OB",
                                          [verify_ent("OB InstrType", ob_instr_type.name, instr_type),
                                           verify_ent("OB ExecSts", ob_exec_sts.name, "Filled"),
                                           verify_ent("OB Qty", ob_qty.name, qty)]))


def execute(report_id):
    common_act = Stubs.win_act

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    case_name = "QAP-570"
    quote_owner = "QA2"
    case_instr_type = "Spot"
    case_qty1 = 1000000
    case_qty2 = 11
    case_qty3 = 110.50
    case_tenor = "Spot"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "ASPECT_CITI"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request=ModifyRFQTileRequest(details=base_rfq_details)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_order(base_rfq_details, ar_service, case_qty1, case_from_currency,
                     case_to_currency, case_tenor, case_client)


        #TODO Which variant is best?
        # First
        modify_request.set_quantity(case_qty2)
        call(ar_service.modifyRFQTile,modify_request.build())

        # TODO Second
        # modify_order(base_rfq_details, ar_service, case_qty2, case_from_currency,
        #              case_to_currency, case_tenor, case_client)


        send_rfq(base_rfq_details, ar_service)

        # Step 2
        place_order_tob(base_rfq_details, ar_service)
        check_order_book("OB_0", case_base_request, case_instr_type, common_act, ob_act, '11')
        cancel_rfq(base_rfq_details, ar_service)

        # Step 3
        modify_order(base_rfq_details, ar_service, case_qty3, case_from_currency,
                     case_to_currency, case_tenor, case_client)
        send_rfq(base_rfq_details, ar_service)
        #
        # # Step 4
        place_order_tob(base_rfq_details, ar_service)
        check_order_book("OB_1", case_base_request, case_instr_type, common_act, ob_act, '110.50')
        cancel_rfq(base_rfq_details, ar_service)



    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)
