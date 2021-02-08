import logging
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs

from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodNOSRule, TemplateQuodOCRRRule, TemplateQuodOCRRule

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent, order_analysis_algo_parameters_request, \
    create_order_analysis_events_request, create_verification_request, check_value
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, \
    ExtractionDetail, ExtractionAction, ModifyOrderDetails, CancelOrderDetails
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.rfq_wrappers import RFQTileDetails, RFQTileOrderDetails, RFQTileOrderSide, RFQTilePanelDetails


import rule_management as rm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    core = Stubs.core
    common_act = Stubs.win_act

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-585"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    rfq_service = Stubs.win_act_rfq_service

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    try:
        venue = "HSB"

        # Steps 1-2
        details = RFQTileDetails(base=base_request)
        details.set_from_currency("EUR")
        details.set_to_currency("USD")
        # details.set_settlement_date(bca.get_t_plus_date(2))
        details.set_near_tenor("Spot")
        call(rfq_service.createRFQ, details.request())

        # Check QRB
        # extraction_id = 'QRB_0'
        # qrb = QuoteDetailsRequest(base=base_request)
        # qrb.set_extraction_id(extraction_id)
        # qrb.set_filter(["Venue", "HSBCR"])
        #
        # qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
        # qrb_quote_status = ExtractionDetail("quoteRequestBook.quotestatus", "QuoteStatus")
        # qrb.add_extraction_detail(qrb_status)
        # qrb.add_extraction_detail(qrb_quote_status)
        #
        # call(rfq_service.getQuoteRequestBookDetails, qrb.request())
        #
        # call(common_act.verifyEntities, verification(extraction_id, "checking QRB",
        #                                              [verify_ent("QRB Status", qrb_status.name, "Test"),
        #                                               verify_ent("QRB QuoteStatus", qrb_quote_status.name, "Test")]))

        # Step 3
        details = RFQTileOrderDetails(base=base_request)
        details.set_venue(venue)
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

        # Steps 4
        details = RFQTileDetails(base=base_request)
        call(rfq_service.createRFQ, details.request())

        # Step 5
        details = RFQTileOrderDetails(base=base_request)
        details.set_venue(venue)
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

        # Steps 7
        details = RFQTileDetails(base=base_request)
        call(rfq_service.createRFQ, details.request())

        # Step 7
        details = RFQTileOrderDetails(base=base_request)
        details.set_venue(venue)
        details.set_action(RFQTileOrderSide.BUY)
        call(rfq_service.sendRFQOrder, details.request())

        details = RFQTilePanelDetails(base=base_request)
        call(rfq_service.cancelRFQ, details.request())

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [RFQ, TRFQ]:
        rule_manager.remove_rule(rule)

    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
