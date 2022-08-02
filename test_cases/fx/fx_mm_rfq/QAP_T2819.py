import logging
from datetime import date
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def press_pricing(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_pricing()
    call(service.modifyRatesTile, modify_request.build())


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

    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service
    dealer_service = Stubs.win_act_dealer_intervention_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "GBP/USD-1W"
    client_tier = "Iridium1"
    qty = str(randint(1000000, 2000000))
    symbol = "GBP/USD"
    security_type_fwd = "FXFWD"
    settle_date = wk1()
    settle_type = "W1"
    currency = "GBP"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        press_pricing(base_details, cp_service)
        # Step 2
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_fwd, settldate=settle_date, settltype=settle_type,
                                   currency=currency,
                                   account=client_tier)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_no_reply()
        # Step 3
        quote_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty, today)
        # Step 4
        check_dealer_intervention(case_base_request, dealer_service, case_id, quote_id)
        close_dmi_window(case_base_request, dealer_service)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            press_pricing(base_details, cp_service)
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
