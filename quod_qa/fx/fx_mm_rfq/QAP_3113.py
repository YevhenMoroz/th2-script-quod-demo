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
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, SelectRowsRequest
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


def select_row(base_request, service, row_number):
    request = SelectRowsRequest(base_request)
    request.set_row_numbers(row_number)
    call(service.selectRows, request.build())


def press_pricing(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_pricing()
    call(service.modifyRatesTile, modify_request.build())


def check_quote_request_b(base_request, service, case_id, status, auto_q, qty, creation_time, client_tier):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Qty", qty, "CreationTime", creation_time, "ClientTier", client_tier])
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


def check_dealer_intervention(base_request, service, case_id, quote_id, near_qty, far_qty, near_tenor, far_tenor):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Id": quote_id})

    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_id = bca.client_orderid(8)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.status", "Status"))
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.nearLegQty", "NearLegQty"))
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.farLegQty", "FarLegQty"))
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.nearLegTenor", "Near Leg Tenor"))
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.farLegTenor", "Far Leg Tenor"))

    response = call(service.getUnassignedRFQDetails, extraction_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check quote request in DI")
    verifier.compare_values("Status", "New", response["dealerIntervention.status"])
    verifier.compare_values("NearLegQty", near_qty, response["dealerIntervention.nearLegQty"].replace(",", ""))
    verifier.compare_values("FarLegQty", far_qty, response["dealerIntervention.farLegQty"].replace(",", ""))
    verifier.compare_values("Near Leg Tenor", near_tenor, response["dealerIntervention.nearLegTenor"])
    verifier.compare_values("Far Leg Tenor", far_tenor, response["dealerIntervention.farLegTenor"])
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
    instrument = "EUR/USD-1W"
    client_tier = "Argentina"
    client = "Argentina1"

    qty = "2000000"
    qty_2 = "3000000"
    symbol = "EUR/USD"
    settle_date_w1 = wk1()
    settle_date_w2 = wk2()
    security_type_swap = "FXSWAP"
    security_type_fwd = "FXFWD"
    settle_type_w1 = "W1"
    settle_type_w2 = "W2"
    currency = "EUR"
    settle_currency = "USD"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        select_row(base_details, cp_service, [2, 3])
        press_pricing(base_details, cp_service)
        # Step 2
        params_swap = CaseParamsSellRfq(client, case_id, side="2", leg1_side="1", leg2_side="2",
                                        orderqty=qty_2, leg1_ordqty=qty, leg2_ordqty=qty_2,
                                        currency=currency, settlcurrency=settle_currency,
                                        leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                        settldate=settle_date_w1, leg1_settldate=settle_date_w1,
                                        leg2_settldate=settle_date_w2,
                                        symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                        securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                        leg2_securitytype=security_type_fwd,
                                        securityid=symbol)

        rfq = FixClientSellRfq(params_swap)
        rfq.send_request_for_quote_swap_no_reply()
        # Step 3
        qr_id = check_quote_request_b(case_base_request, ar_service, case_id, "New", "No", qty_2, today, client_tier)
        check_dealer_intervention(case_base_request, dealer_service, case_id, qr_id, qty, qty_2, "1W", "2W")
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
