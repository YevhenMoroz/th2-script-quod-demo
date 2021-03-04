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


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_order(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_order(base_request, service, qty, cur1, cur2, tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order(base_request, service, venue):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_venue(venue)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_qrb(ex_id, base_request, service, act):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_extraction_id(ex_id)
    qrb.set_filter(["Venue", "HSBC"])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    call(service.getQuoteRequestBookDetails, qrb.request())
    call(act.verifyEntities, verification(ex_id, "checking QRB",
                                          [verify_ent("QRB Venue", qrb_venue.name, "HSBCR"),
                                           verify_ent("QRB Status", qrb_status.name, "New"),
                                           verify_ent("QRB QuoteStatus", qrb_quote_status.name, "Accepted")]))


def check_qb(ex_id, base_request, service, act, owner):
    qb = QuoteDetailsRequest(base=base_request)
    qb.set_extraction_id(ex_id)
    # qb.set_filter(["Venue", "HSBC"])
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb_id = ExtractionDetail("quoteBook.id", "Id")
    qb.add_extraction_details([qb_owner, qb_quote_status, qb_id])
    data = call(service.getQuoteBookDetails, qb.request())
    # call(service.getQuoteBookDetails, qb.request())
    call(act.verifyEntities, verification(ex_id, "checking QB",
                                          [verify_ent("QB Owner", qb_owner.name, owner),
                                           verify_ent("QB QuoteStatus", qb_quote_status.name, "Accepted")]))
    return data[qb_id.name]


def check_ob(ex_id, base_request, instr_type, act, act_ob, qb_id):
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob_insrt_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_venue = ExtractionDetail("orderBook.venue", "Venue")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_insrt_type,
                                                                                 ob_venue,
                                                                                 ob_exec_sts,
                                                                                 ob_id])))
    call(act_ob.getOrdersDetails, ob.request())
    call(act.verifyEntities, verification(ex_id, "checking OB",
                                          [verify_ent("OB InstrType", ob_insrt_type.name, instr_type),
                                           verify_ent("OB Venue", ob_venue.name, "HSBCR"),
                                           verify_ent("OB ExecSts", ob_exec_sts.name, "Filled"),
                                           verify_ent("OB ID vs QB ID", ob_id.name, qb_id)]))


def execute(report_id):
    common_act = Stubs.win_act

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    # print_active_rules()
    case_name = "QAP-585"
    quote_owner = "QA2"
    case_instr_type = "Spot"
    case_venue = "HSBC"
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_far_tenor = "1W"
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

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Steps 1-2
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_order(base_rfq_details, ar_service, case_qty, case_from_currency,
                     case_to_currency, case_near_tenor, case_client)
        # send_order(base_rfq_details, ar_service)
        # check_qrb("QRB_0", case_base_request, ar_service, common_act)
        # qb_quote_id = check_qb("QB_0", case_base_request, ar_service, common_act, quote_owner)

        # Step 3
        # place_order(base_rfq_details, ar_service, case_venue)
        #
        # check_ob("OB_0", case_base_request, case_instr_type, common_act, ob_act, qb_quote_id)
        # #
        # # # call(ar_service.cancelRFQ, base_rfq_details.build())
        # cancel_rfq(base_rfq_details, ar_service)
        #
        # Step 4
        # send_order(base_rfq_details, ar_service)
        # check_qrb("QRB_1", case_base_request, ar_service, common_act)
        # qb_quote_id = check_qb("QB_1", case_base_request, ar_service, common_act, quote_owner)
        #
        # # Step 5
        # place_order(base_rfq_details, ar_service, case_venue)
        # cancel_rfq(base_rfq_details, ar_service)
        # check_ob("OB_1", case_base_request, case_instr_type, common_act, ob_act, qb_quote_id)
        #
        # # Step 6
        # send_order(base_rfq_details, ar_service)
        # check_qrb("QRB_2", case_base_request, ar_service, common_act)
        # qb_quote_id = check_qb("QB_2", case_base_request, ar_service, common_act, quote_owner)
        #
        # # Step 7
        # place_order(base_rfq_details, ar_service, case_venue)
        # cancel_rfq(base_rfq_details, ar_service)
        # check_ob("OB_2", case_base_request, case_instr_type, common_act, ob_act, qb_quote_id)

        # close_fe_2(case_id, session_id)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)
