import logging
import random
from pathlib import Path
import time
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from custom.tenor_settlement_date import spo, wk1
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import get_base_request, call


client = "AURUM1"
account_client = "AURUM1_1"
account_quod = "QUOD4_1"
symbol = "EUR/USD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "EUR"
settle_currency = "USD"
side = "1"
qty_1 = str(random.randint(1000000, 2000000))
qty_2 = "2000000"
qty_total = str(int(qty_1)+int(qty_2))
origin_fix = 'FIX'
origin_int = 'Internal'
side_buy = "Buy"
side_sell = "Sell"


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", 'Position')
    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    time.sleep(0.5)
    return float(response["dealingpositions.position"].replace(",", ""))


def compare_position(even_name, case_id, expected_pos, actual_pos):
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values("Quote position", str(float(expected_pos)), str(actual_pos))

    verifier.verify()


def check_trades_book(base_request, ob_act, origin, qty, trade_side):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["Origin", origin])
    execution_details.set_filter(["Qty", qty])
    execution_details.set_filter(["Side", trade_side])
    trades_id = ExtractionDetail("tradeBook.ExecID", "ExecID")
    trades_qty = ExtractionDetail("tradeBook.Qty", "Qty")
    trades_side = ExtractionDetail("tradeBook.Side", "Side")
    trades_origin = ExtractionDetail("tradeBook.Origin", "Origin")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_id,
                                                                                 trades_qty,
                                                                                 trades_origin,
                                                                                 trades_side])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())

    return [response[trades_id.name], response[trades_origin.name],
            response[trades_side.name], response[trades_qty.name]]


def check_trades_book_ah(base_request, ob_act, case_id, qty):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["Origin", 'AutoHedger'])
    execution_details.set_filter(["Qty", qty])
    trades_id = ExtractionDetail("tradeBook.ExecID", "ExecID")
    trades_qty = ExtractionDetail("tradeBook.Qty", "Qty")
    trades_side = ExtractionDetail("tradeBook.Side", "Side")
    trades_origin = ExtractionDetail("tradeBook.Origin", "Origin")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_id,
                                                                                 trades_qty,
                                                                                 trades_origin,
                                                                                 trades_side])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking that AH order executed with buy Side only')
    verifier.compare_values("ID", 'not null', response[trades_id.name], VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Qty", qty, response[trades_qty.name].replace(',', ''))
    verifier.compare_values("Side", 'Buy', response[trades_side.name])
    verifier.verify()



def compare_orders(case_id, even_name, order_info_1, order_info_2):
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values("ID",order_info_1[0] , order_info_2[0], VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Origin",order_info_1[1] , order_info_2[1], VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Side",order_info_1[2] , order_info_2[2], VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Qty",order_info_1[3] , order_info_2[3])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    pos_service = Stubs.act_fx_dealing_positions
    case_base_request = get_base_request(session_id, case_id)
    ob_act = Stubs.win_act_order_book
    try:
        # Step 7
        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_1, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

        # Step 8
        actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        compare_position('Checking positions Client AURUM1_1', case_id, qty_1, actual_pos_client)
        actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        compare_position('Checking positions Quod QUOD4_1', case_id, f'-{qty_1}', actual_pos_quod)

        fix_order = check_trades_book(case_base_request, ob_act, origin_fix, qty_1, side_buy)
        internal_order= check_trades_book(case_base_request, ob_act, origin_int, qty_1, side_sell)
        compare_orders(case_id, 'Checking that there is two orders with same Qty on opposite sides',
                       fix_order, internal_order)

        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_2, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

        check_trades_book_ah(case_base_request, ob_act, case_id, qty_total)

        actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        compare_position('Checking positions Client AURUM1_1', case_id, qty_total, actual_pos_client)
        actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        compare_position('Checking positions Quod QUOD4_1', case_id, '0', actual_pos_quod)

        # PostConditions
        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_total, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side='2',
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("BidPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
