import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def check_trades_book(base_request, ob_act, case_id, qty, price):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["Qty", qty])
    trades_price = ExtractionDetail("tradeBook.price", "ExecPrice")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_price])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Trade Book")
    verifier.compare_values("Price", price, response[trades_price.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    ob_act = Stubs.win_act_order_book

    client_tier = "Iridium1"
    account = "Iridium1_1"
    symbol = "EUR/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    settle_type_spo = "0"
    currency = "EUR"
    settle_currency = "USD"
    qty_1 = random_qty(1, 2, 7)

    side = "1"

    try:
        # Step 1-2
        params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account)

        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price)
        rfq.verify_order_pending().verify_order_filled()
        check_trades_book(case_base_request, ob_act, case_id, qty_1, price)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
