import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_ndf, wk1_ndf
from custom.verifier import Verifier
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request

from win_gui_modules.wrappers import set_base


def check_quote_book(base_request, service, case_id, qty):
    qb = QuoteDetailsRequest(base=base_request)
    ex_id = bca.client_orderid(4)
    qb.set_extraction_id(ex_id)
    qb.set_filter(["OrdQty", qty])
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb.add_extraction_detail(qb_quote_status)
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values("QuoteStatus", "Rejected", response[qb_quote_status.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    case_base_request = get_base_request(session_id, case_id)


    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty_1 = random_qty(1, 3, 7)
    symbol = "USD/PHP"
    security_type_swap = "FXNDS"
    security_type_fwd = "FXNDF"
    security_type_spo = "FXSPOT"
    settle_date = spo_ndf()
    leg2_settle_date = wk1_ndf()
    settle_type_leg1 = "0"
    settle_type_leg2 = "W1"
    currency = "USD"
    settle_currency = "PHP"

    side = "2"
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
                                   securitytype=security_type_swap, leg1_securitytype=security_type_spo,
                                   leg2_securitytype=security_type_fwd,
                                   securityid=symbol, account=account)

        rfq_swap = FixClientSellRfq(params)
        rfq_swap.send_request_for_quote_swap()
        # Step 2
        rfq_swap.verify_quote_reject()
        # TODO Wait until PMASTER-1842
        check_quote_book(case_base_request, ar_service, case_id, qty_1)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
