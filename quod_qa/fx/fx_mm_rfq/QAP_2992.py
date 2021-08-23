import logging
from datetime import date
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, wk2
from custom.verifier import Verifier
from quod_qa.common_tools import random_qty, parse_qty_from_di, round_decimals_down
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


def extract_qty(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_near_leg_quantity("rfqDetails.nearLegQty")
    extraction_request.extract_far_leg_quantity("rfqDetails.farLegQty")
    response = call(service.getRFQDetails, extraction_request.build())

    near_leg_qty = response["rfqDetails.nearLegQty"]
    far_leg_qty = response["rfqDetails.farLegQty"]
    near_leg_qty = float(parse_qty_from_di(near_leg_qty))
    far_leg_qty = float(parse_qty_from_di(far_leg_qty))
    return [near_leg_qty, far_leg_qty]


def extract_bid_part(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_bid_near_price_value_label("rfqDetails.bidNearPrice")
    extraction_request.extract_bid_far_price_value_label("rfqDetails.bidFarPrice")
    extraction_request.extract_opposite_near_bid_qty_value_label("rfqDetails.nearBidQty")
    extraction_request.extract_opposite_far_bid_qty_value_label("rfqDetails.farBidQty")

    response = call(service.getRFQDetails, extraction_request.build())

    print(response)
    bid_near_px = float(response["rfqDetails.bidNearPrice"])
    bid_far_px = float(response["rfqDetails.bidFarPrice"])
    bid_near_qty = float(parse_qty_from_di(response["rfqDetails.nearBidQty"]))
    bid_far_qty = float(parse_qty_from_di(response["rfqDetails.farBidQty"]))
    return [bid_near_px, bid_far_px, bid_near_qty, bid_far_qty]


def extract_ask_part(base_request, service):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_ask_near_price_value_label("rfqDetails.askNearPrice")
    extraction_request.extract_ask_far_price_value_label("rfqDetails.askFarPrice")
    extraction_request.extract_opposite_near_ask_qty_value_label("rfqDetails.nearAskQty")
    extraction_request.extract_opposite_far_ask_qty_value_label("rfqDetails.farAskQty")

    response = call(service.getRFQDetails, extraction_request.build())

    print(response)

    ask_near_px = float(response["rfqDetails.askNearPrice"])
    ask_far_px = float(response["rfqDetails.askFarPrice"])
    ask_near_qty = float(parse_qty_from_di(response["rfqDetails.nearAskQty"]))
    ask_far_qty = float(parse_qty_from_di(response["rfqDetails.farAskQty"]))
    return [ask_near_px, ask_far_px, ask_near_qty, ask_far_qty]


def modify_price_by_clicking_arrow(base_request, service, pips):
    modify_request = ModificationRequest(base=base_request)
    modify_request.set_spread_step(pips)
    modify_request.widen_spread()
    call(service.modifyAssignedRFQ, modify_request.build())


def modify_price(base_request, service, price):
    modify_request = ModificationRequest(base=base_request)
    modify_request.set_ask_large(price)
    modify_request.set_bid_large(price)
    call(service.modifyAssignedRFQ, modify_request.build())


def check_calculation_near(case_id, event_name, near_px, near_leg_qty, near_qty):
    expected_near_qty = near_px * near_leg_qty
    expected_near_qty = round_decimals_down(expected_near_qty, 2)

    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    verifier.compare_values("Near Qty", str(expected_near_qty), str(near_qty))
    verifier.verify()


def check_calculation_far(case_id, event_name, far_px, far_leg_qty, far_qty):
    expected_far_qty = far_px * far_leg_qty
    expected_far_qty = round_decimals_down(expected_far_qty, 2)

    verifier = Verifier(case_id)
    verifier.set_event_name(event_name)
    verifier.compare_values("Far Qty", str(expected_far_qty), str(far_qty))
    verifier.verify()


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    dealer_service = Stubs.win_act_dealer_intervention_service

    case_base_request = get_base_request(session_id, case_id)
    qty_1 = "20000000"
    qty_2 = "30000000"

    client_tier = "Iridium1"
    account = "Iridium1_1"

    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type_fwd = "FXFWD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    settle_date_w2 = wk2()

    settle_type_spo = "0"
    settle_type_w2 = "W2"
    currency = "GBP"
    settle_currency = "USD"

    side = "1"
    leg1_side = "2"
    leg2_side = "1"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    try:
        # Step 1
        params_swap = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                        orderqty=qty_1, leg1_ordqty=qty_1, leg2_ordqty=qty_2,
                                        currency=currency, settlcurrency=settle_currency,
                                        leg1_settltype=settle_type_spo, leg2_settltype=settle_type_w2,
                                        settldate=settle_date_spo, leg1_settldate=settle_date_spo,
                                        leg2_settldate=settle_date_w2,
                                        symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                        securitytype=security_type_swap, leg1_securitytype=security_type_spo,
                                        leg2_securitytype=security_type_fwd,
                                        securityid=symbol, account=account)

        rfq = FixClientSellRfq(params_swap)
        rfq.send_request_for_quote_swap_no_reply()
        # Step 2
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", "31000000", today)
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id)
        assign_firs_request(case_base_request, dealer_service)
        # Step 3
        estimate_first_request(case_base_request, dealer_service)
        # Step 4
        qty = extract_qty(case_base_request, dealer_service)
        bid_values = extract_bid_part(case_base_request, dealer_service)
        ask_values = extract_ask_part(case_base_request, dealer_service)
        check_calculation_near(case_id, "Check near bid qty calculation", bid_values[0], qty[0], bid_values[2])
        check_calculation_far(case_id, "Check far bid qty calculation", bid_values[1], qty[1], bid_values[3])
        check_calculation_near(case_id, "Check near ask qty calculation", ask_values[0], qty[0], ask_values[2])
        check_calculation_far(case_id, "Check ask bid qty calculation", ask_values[1], qty[1], ask_values[3])
        # Step 5
        modify_price(case_base_request, dealer_service, "2.36")

        bid_values = extract_bid_part(case_base_request, dealer_service)
        ask_values = extract_ask_part(case_base_request, dealer_service)
        check_calculation_near(case_id, "Check near bid qty calculation after changing price", bid_values[0], qty[0],
                               bid_values[2])
        check_calculation_far(case_id, "Check far bid qty calculation after changing price", bid_values[1], qty[1],
                              bid_values[3])
        check_calculation_near(case_id, "Check near ask qty calculation after changing price", ask_values[0], qty[0],
                               ask_values[2])
        check_calculation_far(case_id, "Check ask bid qty calculation after changing price", ask_values[1], qty[1],
                              ask_values[3])
        # Step 6
        modify_price_by_clicking_arrow(case_base_request, dealer_service, "5")
        bid_values = extract_bid_part(case_base_request, dealer_service)
        ask_values = extract_ask_part(case_base_request, dealer_service)
        check_calculation_near(case_id, "Check near bid qty calculation after changing price by clicking on arrow",
                               bid_values[0], qty[0], bid_values[2])
        check_calculation_far(case_id, "Check far bid qty calculation after changing price by clicking on arrow",
                              bid_values[1], qty[1], bid_values[3])
        check_calculation_near(case_id, "Check near ask qty calculation after changing price by clicking on arrow",
                               ask_values[0], qty[0], ask_values[2])
        check_calculation_far(case_id, "Check ask bid qty calculation after changing price by clicking on arrow",
                              ask_values[1], qty[1], ask_values[3])
        close_dmi_window(case_base_request, dealer_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
