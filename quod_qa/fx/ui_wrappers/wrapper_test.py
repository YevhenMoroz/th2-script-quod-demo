import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3, broken_w1w2
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from quod_qa.fx.ui_wrappers.forex_order_book import FxOrderBook
from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

client_tier = "Iridium1"
account = "Iridium1_1"
symbol = "EUR/USD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "EUR"
settle_currency = "USD"
side = "1"


def check_order_book(base_request, act_ob, case_id, qty):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Qty", qty])
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_exec_sts])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.verify()


def check_quote_book(base_request, service, case_id, status, qty):
    qb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qb.set_extraction_id(extraction_id)
    qb.set_filter(["OrdQty", qty])
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb.add_extraction_details([qb_quote_status])
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values("QuoteStatus", status, response[qb_quote_status.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    act_ob = Stubs.win_act_order_book

    try:
        check_order_book(case_base_request, act_ob, case_id, "1000000")
        check_quote_book(case_base_request, ar_service, case_id, "Canceled", "1000000")
        check_order_book(case_base_request, act_ob, case_id, "99000000")
        check_quote_book(case_base_request, ar_service, case_id, "Canceled", "1000000")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
