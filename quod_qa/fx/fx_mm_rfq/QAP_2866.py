import logging
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2
from custom.verifier import Verifier
from quod_qa.common_tools import shorting_qty_for_di, random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    RFQExtractionDetailsRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def check_dealer_intervention(base_request, service, case_id, qty):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_dict({"Qty": qty})
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


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def check_qty_near_leg(base_request, service, case_id, near_qty):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_near_leg_quantity("rfqDetails.nearLegQty")
    response = call(service.getRFQDetails, extraction_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check displaying Uneven Swap Qty")
    verifier.compare_values("Near leg qty", near_qty, response["rfqDetails.nearLegQty"])
    verifier.verify()


def check_qty_far_leg(base_request, service, case_id, far_qty):
    extraction_request = RFQExtractionDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.extract_far_leg_quantity("rfqDetails.farLegQty")
    response = call(service.getRFQDetails, extraction_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check displaying Uneven Swap Qty")
    verifier.compare_values("Far leg qty", far_qty, response["rfqDetails.farLegQty"])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    dealer_service = Stubs.win_act_dealer_intervention_service

    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty_1 = random_qty(1, 10, 9)
    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type = "FXFWD"
    settle_date = wk1()
    leg2_settle_date = wk2()
    settle_type_leg1 = "W1"
    settle_type_leg2 = "W2"
    currency = "GBP"
    settle_currency = "USD"
    expected_1 = shorting_qty_for_di(qty_1, currency)

    side = ""
    leg1_side = "1"
    leg2_side = "2"

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty_1, leg1_ordqty=qty_1, leg2_ordqty=qty_1,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap_no_reply()
        # Step 2
        check_dealer_intervention(case_base_request, dealer_service, case_id, qty_1)
        assign_firs_request(case_base_request, dealer_service)
        # Step 3
        estimate_first_request(case_base_request, dealer_service)
        # Step 4
        check_qty_near_leg(case_base_request, dealer_service, case_id, expected_1)
        # TODO Check if far leg exist

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            close_dmi_window(case_base_request, dealer_service)
        except Exception:
            logging.error("Error execution", exc_info=True)
