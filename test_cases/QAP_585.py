import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs

from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.rfq_wrappers import RFQTileDetails, RFQTileOrderDetails, RFQTileOrderSide, RFQTilePanelDetails

import rule_management as rm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def send_rfq(br, service):
    details = RFQTileDetails(base=br)
    call(service.createRFQ, details.request())


def send_order(ex_id):
    details = RFQTileOrderDetails(base=base_request)
    details.set_venue(venue)
    details.set_action(RFQTileOrderSide.BUY)
    call(rfq_service.sendRFQOrder, details.request())


def cancel_rfq(ex_id):
    pass


def check_qrb(ex_id, br, service, act):
    qrb = QuoteDetailsRequest(base=br)
    qrb.set_extraction_id(ex_id)
    # qrb.set_filter(["Venue", "HSBCR"])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    call(service.getQuoteRequestBookDetails, qrb.request())
    call(act.verifyEntities, verification(ex_id, "checking QRB",
                                          [verify_ent("QRB Venue", qrb_venue.name, "HSBCR"),
                                           verify_ent("QRB Status", qrb_status.name, "New"),
                                           verify_ent("QRB QuoteStatus", qrb_quote_status.name, "Accepted")]))


def check_qb(ex_id, br, service, act, owner):
    qb = QuoteDetailsRequest(base=br)
    qb.set_extraction_id(ex_id)
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb.add_extraction_details([qb_owner, qb_quote_status])
    call(service.getQuoteBookDetails, qb.request())
    call(act.verifyEntities, verification(ex_id, "checking QB",
                                          [verify_ent("QB Owner", qb_owner.name, owner),
                                           verify_ent("QB QuoteStatus", qb_quote_status.name, "Accepted")]))


def execute(report_id):
    common_act = Stubs.win_act

    # Rules
    # rule_manager = rm.RuleManager()
    # RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    # TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-585"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    rfq_service = Stubs.win_act_rfq_service
    ob_act = Stubs.win_act_order_book

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    try:
        quote_owner = "dshepelev"
        instr_type = "Spot"
        venue = "HSB"

        # Steps 1-2
        send_rfq(base_request, rfq_service)
        check_qrb("QRB_0", base_request, rfq_service, common_act)
        check_qb("QB_0", base_request, rfq_service, common_act, quote_owner)

        # not refactored section
        # Step 3
        details = RFQTileOrderDetails(base=base_request)
        details.set_venue(venue)
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

        # Check OB
        extraction_id = 'OB_0'
        ob = OrdersDetails()
        ob.set_default_params(base_request)
        ob.set_extraction_id(extraction_id)
        ob_insrt_type = ExtractionDetail("orderBook.instrtype", "InstrType")
        ob_venue = ExtractionDetail("orderBook.venue", "Venue")
        ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
        ob.add_single_order_info(
            OrderInfo.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[ob_insrt_type,
                                                                                     ob_venue,
                                                                                     ob_exec_sts])))

        call(ob_act.getOrdersDetails, ob.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking OB",
                                                     [verify_ent("OB InstrType", ob_insrt_type.name, instr_type),
                                                      verify_ent("OB Venue", ob_venue.name, "HSBCR"),
                                                      verify_ent("OB ExecSts", ob_exec_sts.name, "Filled")]))

        # Step 4
        details = RFQTileDetails(base=base_request)
        call(rfq_service.createRFQ, details.request())

        # Check QRB
        extraction_id = 'QRB_1'
        qrb = QuoteDetailsRequest(base=base_request)
        qrb.set_extraction_id(extraction_id)

        # qrb.set_filter(["Venue", "HSBCR"])
        qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
        qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
        qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
        qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])

        call(rfq_service.getQuoteRequestBookDetails, qrb.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking QRB",
                                                     [verify_ent("QRB Venue", qrb_venue.name, "HSBCR"),
                                                      verify_ent("QRB Status", qrb_status.name, "New"),
                                                      verify_ent("QRB QuoteStatus", qrb_quote_status.name,
                                                                 "Accepted")]))

        # Check QB
        extraction_id = 'QB_1'
        qb = QuoteDetailsRequest(base=base_request)
        qb.set_extraction_id(extraction_id)
        qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
        qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
        qb.add_extraction_details([qb_owner, qb_quote_status])

        call(rfq_service.getQuoteBookDetails, qb.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking QB",
                                                     [verify_ent("QB Owner", qb_owner.name, quote_owner),
                                                      verify_ent("QB QuoteStatus", qb_quote_status.name,
                                                                 "Accepted")]))

        # Step 5
        details = RFQTileOrderDetails(base=base_request)
        details.set_venue(venue)
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

        # Check OB
        extraction_id = 'OB_0'
        ob = OrdersDetails()
        ob.set_default_params(base_request)
        ob.set_extraction_id(extraction_id)
        ob_insrt_type = ExtractionDetail("orderBook.instrtype", "InstrType")
        ob_venue = ExtractionDetail("orderBook.venue", "Venue")
        ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
        ob.add_single_order_info(
            OrderInfo.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[ob_insrt_type,
                                                                                     ob_venue,
                                                                                     ob_exec_sts])))

        call(ob_act.getOrdersDetails, ob.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking OB",
                                                     [verify_ent("OB InstrType", ob_insrt_type.name, instr_type),
                                                      verify_ent("OB Venue", ob_venue.name, "HSBCR"),
                                                      verify_ent("OB ExecSts", ob_exec_sts.name, "Filled")]))

        # Steps 7
        details = RFQTileDetails(base=base_request)
        call(rfq_service.createRFQ, details.request())

        # Check QRB
        extraction_id = 'QRB_1'
        qrb = QuoteDetailsRequest(base=base_request)
        qrb.set_extraction_id(extraction_id)

        # qrb.set_filter(["Venue", "HSBCR"])
        qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
        qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
        qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
        qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])

        call(rfq_service.getQuoteRequestBookDetails, qrb.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking QRB",
                                                     [verify_ent("QRB Venue", qrb_venue.name, "HSBCR"),
                                                      verify_ent("QRB Status", qrb_status.name, "New"),
                                                      verify_ent("QRB QuoteStatus", qrb_quote_status.name,
                                                                 "Accepted")]))

        # Check QB
        extraction_id = 'QB_1'
        qb = QuoteDetailsRequest(base=base_request)
        qb.set_extraction_id(extraction_id)
        qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
        qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
        qb.add_extraction_details([qb_owner, qb_quote_status])

        call(rfq_service.getQuoteBookDetails, qb.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking QB",
                                                     [verify_ent("QB Owner", qb_owner.name, quote_owner),
                                                      verify_ent("QB QuoteStatus", qb_quote_status.name,
                                                                 "Accepted")]))

        # Step 8
        details = RFQTileOrderDetails(base=base_request)
        details.set_venue(venue)
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

        # Check OB
        extraction_id = 'OB_0'
        ob = OrdersDetails()
        ob.set_default_params(base_request)
        ob.set_extraction_id(extraction_id)
        ob_insrt_type = ExtractionDetail("orderBook.instrtype", "InstrType")
        ob_venue = ExtractionDetail("orderBook.venue", "Venue")
        ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
        ob.add_single_order_info(
            OrderInfo.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[ob_insrt_type,
                                                                                     ob_venue,
                                                                                     ob_exec_sts])))

        call(ob_act.getOrdersDetails, ob.request())

        call(common_act.verifyEntities, verification(extraction_id, "checking OB",
                                                     [verify_ent("OB InstrType", ob_insrt_type.name, instr_type),
                                                      verify_ent("OB Venue", ob_venue.name, "HSBCR"),
                                                      verify_ent("OB ExecSts", ob_exec_sts.name, "Filled")]))

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    # for rule in [RFQ, TRFQ]:
    #     rule_manager.remove_rule(r