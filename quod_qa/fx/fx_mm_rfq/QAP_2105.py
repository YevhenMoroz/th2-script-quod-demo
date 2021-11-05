import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_ndf, wk1_ndf
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request

from win_gui_modules.wrappers import set_base


def check_order_book(base_request, act_ob, case_id, qty, currency):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Qty", qty])
    ob_side = ExtractionDetail("orderBook.side", "Side")
    ob_ord_type = ExtractionDetail("orderBook.ordType", "OrdType")
    ob_currency = ExtractionDetail("orderBook.currency", "Currency")
    ob_instr_type = ExtractionDetail("orderBook.instrType", "InstrType")
    ob_exec_status= ExtractionDetail("orderBook.sts", "ExecSts")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[ob_side, ob_ord_type, ob_currency, ob_instr_type, ob_exec_status])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check order book")
    verifier.compare_values("Order side", "Sell", response[ob_side.name])
    verifier.compare_values("Order type", "PreviouslyQuoted", response[ob_ord_type.name])
    verifier.compare_values("Order currency", currency, response[ob_currency.name])
    verifier.compare_values("Order InstrType", "FXNDS", response[ob_instr_type.name])
    verifier.compare_values("Order status", "Filled", response[ob_exec_status.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ob_service = Stubs.win_act_order_book
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
    currency = "PHP"
    settle_currency = "USD"

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
        rfq_swap.verify_quote_pending_swap()
        price = rfq_swap.extract_filed("BidPx")
        # Step 2
        rfq_swap.send_new_order_multi_leg(price)
        # Step 3
        rfq_swap.verify_order_pending_swap()
        rfq_swap.verify_order_filled_swap()
        # Step 4
        check_order_book(case_base_request, ob_service, case_id, qty_1, currency)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
