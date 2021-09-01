import logging
import time
from datetime import date
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1
from custom.verifier import Verifier
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    RFQExtractionDetailsRequest, ModificationRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def check_quote_request_b(base_request, service, case_id, status, auto_q, qty, creation_time):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Qty", qty, "CreationTime", creation_time])
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_auto_quoting = ExtractionDetail("quoteRequestBook.autoQuoting", "AutomaticQuoting")
    qr_id = ExtractionDetail("quoteRequestBook.id", "Id")
    qr_c_id = ExtractionDetail("dealerInterventionClQuote", "ClQuoteReqID")
    qrb.add_extraction_details([qrb_status, qrb_auto_quoting, qr_id, qr_c_id])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values("Status", status, response[qrb_status.name])
    verifier.compare_values("AutomaticQuoting", auto_q, response[qrb_auto_quoting.name])
    verifier.verify()
    quote_id = response[qr_id.name]
    client_quote_id=response[qr_c_id.name]
    return [quote_id, client_quote_id]


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
    return response["dealerInterventionClQuote"]


def assign_firs_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.assignToMe, base_data.build())


def estimate_first_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.estimate, base_data.build())


def extract_bid_part(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_bid_price_pips("rfqDetails.PricePips")
    extraction_request.extract_bid_price_large("rfqDetails.PriceLarge")
    response = call(service.getRFQDetails, extraction_request.build())
    bid_large = response["rfqDetails.PriceLarge"]
    bid_small = response["rfqDetails.PricePips"]
    bid_spot_rate = bid_large + bid_small
    return bid_spot_rate


def extract_ask_part(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_ask_price_pips("rfqDetails.askPricePips")
    extraction_request.extract_ask_price_large("rfqDetails.askPriceLarge")
    response = call(service.getRFQDetails, extraction_request.build())
    print(response)
    ask_large = response["rfqDetails.askPriceLarge"]
    ask_small = response["rfqDetails.askPricePips"]
    ask_spot_rate = ask_large + ask_small
    return ask_spot_rate


def send_quote_from_dealer(base_request, service):
    modify_request = ModificationRequest(base=base_request)
    modify_request.send()
    call(service.modifyAssignedRFQ, modify_request.build())


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    dealer_service = Stubs.win_act_dealer_intervention_service

    connectivityRFQ = 'fix-ss-rfq-314-luna-standard'
    case_base_request = get_base_request(session_id, case_id)
    verifier = Stubs.verifier
    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty = random_qty(2, 3, 8)
    symbol = "EUR/GBP"
    security_type_fwd = "FXFWD"
    settle_date = wk1()
    currency = "EUR"
    settle_currency="GBP"
    settle_type = "W1"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol, side="1",
                                   securitytype=security_type_fwd, settldate=settle_date, settltype=settle_type,
                                   currency=currency, settlcurrency=settle_currency, securityid=symbol,
                                   account=account)

        rfq = FixClientSellRfq(params)

        rfq.send_request_for_quote_no_reply()
        # Step 2
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty, today)
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id[0])
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        time.sleep(5)
        # Step 3
        bid_values = extract_bid_part(case_base_request, dealer_service)
        ask_values = extract_ask_part(case_base_request, dealer_service)
        print(ask_values)
        #
        print("PRESS SEND")
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint
        send_quote_from_dealer(case_base_request, dealer_service)
        time.sleep(10)
        rfq.verify_quote_pending(checkpoint_id_=checkpoint_id1)

        # TODO Need to receive QuoteID for sending NewOrderSingle

        rfq.send_new_order_single("1.1818")
        rfq.verify_order_pending().verify_order_filled_fwd()
        close_dmi_window(case_base_request, dealer_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
