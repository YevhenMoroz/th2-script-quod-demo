import logging
from datetime import date
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest
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


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    dealer_service = Stubs.win_act_dealer_intervention_service
    ar_service = Stubs.win_act_aggregated_rates_service
    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty_above_sum = str(randint(17000000, 20000000))
    qty_bellow_sum = str(randint(1000000, 2000000))
    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type = "FXFWD"
    settle_date = wk1()
    leg2_settle_date = wk2()
    settle_type_leg1 = "W1"
    settle_type_leg2 = "W2"
    currency = "GBP"
    settle_currency = "USD"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    side = ""
    leg1_side = "1"
    leg2_side = "2"

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty_above_sum, leg1_ordqty=qty_above_sum, leg2_ordqty=qty_above_sum,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap_no_reply()
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty_above_sum, today)
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id)
        close_dmi_window(case_base_request, dealer_service)
        # Step 2
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty_bellow_sum, leg1_ordqty=qty_bellow_sum, leg2_ordqty=qty_bellow_sum,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap()
        rfq.verify_quote_pending_swap()
        check_quote_request_b(case_base_request, ar_service, case_id, "New", "Yes", qty_bellow_sum, today)
        # Step 3
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty="1000000", leg1_ordqty="1000000", leg2_ordqty="2000000",
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap()
        rfq.verify_quote_pending_swap()
        check_quote_request_b(case_base_request, ar_service, case_id, "New", "Yes", qty_bellow_sum, today)
        # Step 4
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty_bellow_sum, leg1_ordqty=qty_bellow_sum, leg2_ordqty=qty_above_sum,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap_no_reply()
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty_bellow_sum, today)
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id)
        close_dmi_window(case_base_request, dealer_service)
        # Step 5
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty_bellow_sum, leg1_ordqty=qty_above_sum, leg2_ordqty=qty_bellow_sum,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap_no_reply()
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty_bellow_sum, today)
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id)
        close_dmi_window(case_base_request, dealer_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
