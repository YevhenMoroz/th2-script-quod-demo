import logging
from pathlib import Path

from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction, PlaceRFQRequest, \
    RFQTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.layout_panel_wrappers import WorkspaceModificationRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from custom import basic_custom_actions as bca
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def close_tile(self, details):
    call(self.ar_service.closeRFQTile, details.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, near_qty, cur1, cur2, near_tenor, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.SELL)
    call(service.placeRFQOrder, rfq_request.build())


def check_quote_request_b(base_request, service, case_id, status, quote_sts, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Venue", venue])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Venue', venue + "R", response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values("QuoteStatus", quote_sts, response[qrb_quote_status.name])
    verifier.verify()


def check_quote_book(base_request, service, case_id, owner):
    qb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qb.set_extraction_id(extraction_id)
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb.add_extraction_details([qb_owner, qb_quote_status])
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values('Owner', owner, response[qb_owner.name])
    verifier.compare_values('QuoteStatus', 'Terminated', response[qb_quote_status.name])
    verifier.verify()


def check_order_book(base_request, instr_type, act_ob, case_id, qty):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_type = ExtractionDetail("orderBook.ordtype", "OrdType")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_type,
                                                                                 ob_qty])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('InstrType', instr_type, response[ob_instr_type.name])
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.compare_values('OrdType', 'PreviouslyQuoted', response[ob_type.name])
    verifier.compare_values("Qty", str(qty), response[ob_qty.name].replace(',', ''))
    verifier.verify()


def import_layout(base_request, option_service):
    modification_request = WorkspaceModificationRequest()
    modification_request.set_default_params(base_request=base_request)
    modification_request.set_filename("rfq_workspace.xml")
    modification_request.set_path('C:\\QA')
    modification_request.do_import()

    call(option_service.modifyWorkspace, modification_request.build())


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    option_service = Stubs.win_act_options

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_tenor = "Spot"
    case_venue = ["CITI"]
    case_filter_venue = "CITI"
    case_qty = 2000000
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"
    case_instr_type = 'Spot'
    quote_owner = Stubs.custom_config['qf_trading_fe_user']

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        
        # Step 1
        import_layout(case_base_request, option_service)
        # Step 2-3
        create_or_get_rfq(base_rfq_details, ar_service)
        # Step 4
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                        case_near_tenor, case_client, case_venue)
        # Step 5
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b(case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_filter_venue)
        # Step 6
        place_order_tob(base_rfq_details, ar_service)
        check_order_book(case_base_request, case_instr_type, ob_act, case_id,
                         case_qty)
        check_quote_book(case_base_request, ar_service, case_id, quote_owner)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
