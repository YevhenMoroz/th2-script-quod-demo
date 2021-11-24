from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ModificationRequest, \
    ExtractionDetailsRequest
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ClientRFQTileOrderDetails, \
    ModifyClientRFQTileRequest, SelectRowsRequest
import logging
from pathlib import Path
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request


def create_client_rfq_tile(service, base_tile_data):
    call(service.createClientRFQTile, base_tile_data)


def modify_client_rfq_tile(service, base_tile_data, client_tier, from_curr, to_curr, qty, client, tenor):
    request = ModifyClientRFQTileRequest(data=base_tile_data)
    request.change_client_tier(client_tier)
    request.set_from_curr(from_curr)
    request.set_to_curr(to_curr)
    request.change_near_leg_aty(qty)
    request.change_client(client)
    call(service.modifyRFQTile, request.build())


def send_client_rfq(service, base_tile_data):
    call(service.sendRFQOrder, base_tile_data)


def place_client_rfq_order(service, base_tile_data):
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    requests.set_action_sell()
    call(service.placeClientRFQOrder, requests.build())


def check_dealer_intervention(base_request, service, case_id, quote_id):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Id": quote_id})

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_id = bca.client_orderid(8)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.status", "Status"))

    response = call(service.getUnassignedRFQDetails, extraction_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check quote request in DI")
    verifier.compare_values("Status", "New", response["dealerIntervention.status"])
    verifier.verify()


def assign_firs_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.assignToMe, base_data.build())


def estimate_first_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.estimate, base_data.build())


def set_ttl_and_send_quote(base_request, service, ttl):
    modify_request = ModificationRequest(base=base_request)
    modify_request.set_quote_ttl(ttl)
    modify_request.send()
    call(service.modifyAssignedRFQ, modify_request.build())


def check_quote_request_b(base_request, service, case_id, status, auto_q, qty, creation_time):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Qty", qty, "CreationTime", creation_time])
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_auto_quoting = ExtractionDetail("quoteRequestBook.autoQuoting", "AutomaticQuoting")
    qr_id = ExtractionDetail("quoteRequestBook.id", "Id")
    qrb.add_extraction_details([qrb_status, qrb_auto_quoting, qr_id])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values("Status", status, response[qrb_status.name])
    verifier.compare_values("AutomaticQuoting", auto_q, response[qrb_auto_quoting.name])
    verifier.verify()
    quote_id = response[qr_id.name]
    return quote_id


def check_order_book(base_request, act_ob, case_id, qty, venue):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Qty", qty])
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_venue = ExtractionDetail("orderBook.venue", "Venue")
    ob_tenor = ExtractionDetail("orderBook.tenor", "Tenor")
    ob_ord_type = ExtractionDetail("orderBook.ordType", "OrdType")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_venue,
                                                                                 ob_exec_sts,
                                                                                 ob_tenor,
                                                                                 ob_ord_type])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])

    verifier.verify()

# TODO Need to add function to work with Client RFQ table