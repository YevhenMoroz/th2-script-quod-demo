import logging
import time
from datetime import date
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    RFQExtractionDetailsRequest
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
    qrb.add_extraction_details([qrb_status, qrb_auto_quoting, qr_id])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values("Status", status, response[qrb_status.name])
    verifier.compare_values("AutomaticQuoting", auto_q, response[qrb_auto_quoting.name])
    verifier.verify()
    quote_id = response[qr_id.name]
    return quote_id


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


def extract_bid_part(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_bid_price_pips("rfqDetails.PricePips")
    extraction_request.extract_bid_price_large("rfqDetails.PriceLarge")
    extraction_request.extract_bid_near_points_value_label("rfqDetails.NearPoints")
    extraction_request.extract_bid_value_label("rfqDetails.Value")
    response = call(service.getRFQDetails, extraction_request.build())
    print(response)
    bid_large = response["rfqDetails.PriceLarge"]
    bid_small = response["rfqDetails.PricePips"]
    bid_spot_rate = bid_large + bid_small
    bid_near_pts = response["rfqDetails.NearPoints"]
    bid_px = response["rfqDetails.Value"]
    return [bid_spot_rate, bid_near_pts, bid_px]


def extract_ask_part(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_ask_price_pips("rfqDetails.askPricePips")
    extraction_request.extract_ask_price_large("rfqDetails.askPriceLarge")
    extraction_request.extract_ask_near_points_value_label("rfqDetails.askNearPoints")
    extraction_request.extract_ask_value_label("rfqDetails.askValue")
    response = call(service.getRFQDetails, extraction_request.build())
    print(response)
    ask_large = response["rfqDetails.askPriceLarge"]
    ask_small = response["rfqDetails.askPricePips"]
    ask_spot_rate = ask_large + ask_small
    ask_near_pts = response["rfqDetails.askNearPoints"]
    ask_px = response["rfqDetails.askValue"]
    return [ask_spot_rate, ask_near_pts, ask_px]


def check_calculation(case_id, event_name, spot_rate, pts, px):
    pts = float(pts) / 10000
    expected_px = float(spot_rate) + pts

    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    verifier.compare_values("Px value", str(expected_px), str(px))
    verifier.verify()


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service
    dealer_service = Stubs.win_act_dealer_intervention_service

    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    qty = random_qty(2, 3, 8)
    symbol = "GBP/USD"
    security_type_fwd = "FXFWD"
    settle_date = wk1()
    settle_type = "W1"
    currency = "GBP"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_fwd, settldate=settle_date, settltype=settle_type,
                                   currency=currency,
                                   account=client_tier)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_no_reply()
        # Step 2
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty, today)
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id)
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        time.sleep(5)
        # Step 3
        bid_values = extract_bid_part(case_base_request, dealer_service)
        ask_values = extract_ask_part(case_base_request, dealer_service)
        #
        check_calculation(case_id, "Check bid calculation", bid_values[0], bid_values[1], bid_values[2])
        check_calculation(case_id, "Check ask calculation", ask_values[0], ask_values[1], ask_values[2])

        close_dmi_window(case_base_request, dealer_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
