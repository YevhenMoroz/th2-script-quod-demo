import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base

client_tier = "AURUM1"
account = "AURUM1_1"

symbol = "GBP/DKK"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "GBP"
settle_currency = "DKK"

side_b = "1"
side_s = "2"


def send_rfq_and_filled_order_buy(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                    currency=currency, side=side_b,
                                    account=account)

    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()

    rfq.verify_quote_pending()

    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().verify_order_filled()


def send_rfq_and_filled_order_sell(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                    currency=currency, side=side_s,
                                    account=account)

    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()

    rfq.verify_quote_pending()

    price = rfq.extract_filed("BidPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().verify_order_filled()


def check_order_book(base_request, act_ob, orig, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request=base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Orig", orig, "Client ID", client])
    order_id = ExtractionDetail("orderBook.id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_detail=order_id)))
    response = call(act_ob.getOrdersDetails, ob.request())
    return response[order_id.name]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    connectivity_drop_copy = "fix-sell-m-314luna-drop"
    verifier = Stubs.verifier
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ob_service = Stubs.win_act_order_book
    orig = "AutoHedger"
    client = "QUOD4"

    try:
        # Step 1
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint
        send_rfq_and_filled_order_buy(case_id, "1000000")
        order_id = check_order_book(case_base_request, ob_service, orig, client)

        order_params = {
            'ExecID': '*',
            'OrderQty': "1000000",
            'LastQty': "1000000",
            'LastSpotRate': '*',
            'OrderID': order_id,
            'TransactTime': '*',
            'Side': '*',
            'AvgPx': '*',
            'OrdStatus': '2',
            'SettlCurrency': settle_currency,
            'SettlDate': spo(),
            'Currency': currency,
            'TimeInForce': '4',
            'TradeDate': '*',
            'ExecType': 'F',
            'TradeReportingIndicator': '0',
            'HandlInst': '1',
            'LeavesQty': '0',
            'NoParty': [{
                'PartyID': 'AH_TECHNICAL_USER',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'CumQty': "1000000",
            'LastPx': '*',
            'SpotSettlDate': spo(),
            'OrdType': "1",
            'LastMkt': "*",
            'ClOrdID': order_id,
            'QtyType': '*',
            'SettlType': '*',
            'Instrument': {
                'SecurityType': 'FXSPOT',
                'Symbol': symbol,
                'SecurityID': symbol,
                'Product': '4',
                'SecurityIDSource': '8',
                'SecurityExchange': '*'
            },
            'ExDestination': '*',
            'GrossTradeAmt': '*',
        }

        verifier.submitCheckRule(
            bca.create_check_rule("Check Drop Copy Execution Report",
                                  bca.filter_to_grpc('ExecutionReport', order_params, ["OrderID", "ExecType"]),
                                  checkpoint_id1,
                                  connectivity_drop_copy,
                                  case_id)
        )
        send_rfq_and_filled_order_sell(case_id, "1000000")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
