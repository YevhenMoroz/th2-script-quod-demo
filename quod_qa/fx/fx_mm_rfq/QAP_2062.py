import logging
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    ModificationRequest, RFQExtractionDetailsRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def check_dealer_intervention(base_request, service, case_id, qty):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_list(["Qty", qty])
    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_id = bca.client_orderid(8)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.status", "Status"))

    response = call(service.getUnassignedRFQDetails, extraction_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check quote request in DI")
    verifier.compare_values("Status", "New", response["dealerIntervention.status"])


def assign_firs_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.assignToMe, base_data.build())


def estimate_first_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.estimate, base_data.build())


def set_ttl_and_pips(base_request, service, ttl, pips):
    modify_request = ModificationRequest(base=base_request)
    modify_request.set_quote_ttl(ttl)
    modify_request.set_spread_step(pips)
    call(service.modifyAssignedRFQ, modify_request.build())


def modify_spread(base_request, service, *args):
    modify_request = ModificationRequest(base=base_request)
    if "increase_ask" in args:
        modify_request.increase_ask()
    if "decrease_ask" in args:
        modify_request.decrease_ask()
    if "increase_bid" in args:
        modify_request.increase_bid()
    if "decrease_bid" in args:
        modify_request.decrease_bid()
    if "narrow_spread" in args:
        modify_request.narrow_spread()
    if "widen_spread" in args:
        modify_request.widen_spread()
    if "skew_towards_ask" in args:
        modify_request.skew_towards_ask()
    if "skew_towards_bid" in args:
        modify_request.skew_towards_bid()
    call(service.modifyAssignedRFQ, modify_request.build())


def check_ttl(base_request, service, case_id, ttl):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_quote_ttl("rfqDetails.ttl")
    response = call(service.getRFQDetails, extraction_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check quote TTl")
    verifier.compare_values("TTL", ttl, response["rfqDetails.ttl"])
    verifier.verify()


def check_price_ask_pips(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_ask_price_pips("rfqDetails.askPricePips")
    response = call(service.getRFQDetails, extraction_request.build())
    ask = response["rfqDetails.askPricePips"]
    return float(ask)


def check_price_bid_pips(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_bid_price_pips("rfqDetails.bidPricePips")
    response = call(service.getRFQDetails, extraction_request.build())
    bid = response["rfqDetails.bidPricePips"]
    return float(bid)


def compare_prices_ask(case_id, ask_before, ask_after, pips, *args):
    difference = abs(ask_after - ask_before)
    expected_difference = "0.0"
    pips = float(pips) * 10
    if "increase_ask" in args:
        expected_difference = pips
    if "decrease_ask" in args:
        expected_difference = pips
    if "narrow_spread" in args:
        expected_difference = pips
    if "widen_spread" in args:
        expected_difference = pips
    if "skew_towards_ask" in args:
        expected_difference = pips
    if "skew_towards_bid" in args:
        expected_difference = pips

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices ask")
    verifier.compare_values("Price difference", str(expected_difference), str(difference))
    verifier.verify()


def compare_prices_bid(case_id, bid_before, bid_after, pips, *args):
    difference = abs(bid_after - bid_before)
    expected_difference = "0.0"
    pips = float(pips) * 10
    if "increase_bid" in args:
        expected_difference = pips
    if "decrease_bid" in args:
        expected_difference = pips
    if "narrow_spread" in args:
        expected_difference = pips
    if "widen_spread" in args:
        expected_difference = pips
    if "skew_towards_ask" in args:
        expected_difference = pips
    if "skew_towards_bid" in args:
        expected_difference = pips

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices bid")
    verifier.compare_values("Price difference", str(expected_difference), str(difference))
    verifier.verify()


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    dealer_service = Stubs.win_act_dealer_intervention_service

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    qty = str(randint(17000000, 20000000))
    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date = spo()
    settle_type = "SPO"
    currency = "GBP"
    ttl = "360"
    pips = "0.1"
    increase_ask = "increase_ask"
    decrease_ask = "decrease_ask"
    increase_bid = "increase_bid"
    decrease_bid = "decrease_bid"
    narrow_spread = "narrow_spread"
    widen_spread = "widen_spread"
    skew_towards_ask = "skew_towards_ask"
    skew_towards_bid = "skew_towards_bid"
    list_of_actions = [increase_ask, decrease_ask, increase_bid, decrease_bid, narrow_spread,
                       widen_spread, skew_towards_ask, skew_towards_bid]

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency,
                                   account=client_tier)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_no_reply()
        check_dealer_intervention(case_base_request, dealer_service, case_id, qty)
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        # Step 2
        set_ttl_and_pips(case_base_request, dealer_service, ttl, pips)
        check_ttl(case_base_request, dealer_service, case_id, ttl)

        for action in list_of_actions:
            ask = check_price_ask_pips(case_base_request, dealer_service)
            bid = check_price_bid_pips(case_base_request, dealer_service)
            modify_spread(case_base_request, dealer_service, action)
            ask_after = check_price_ask_pips(case_base_request, dealer_service)
            bid_after = check_price_bid_pips(case_base_request, dealer_service)
            compare_prices_ask(case_id, ask, ask_after, pips, action)
            compare_prices_bid(case_id, bid, bid_after, pips, action)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            close_dmi_window(case_base_request, dealer_service)
        except Exception:
            logging.error("Error execution", exc_info=True)
