import logging
from pathlib import Path
import time
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from custom.tenor_settlement_date import spo, wk1
from custom.verifier import Verifier
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import get_base_request, call

client = "AURUM1"
account_client = "AURUM1_1"
account_quod = "QUOD4_1"
account_client_intern = "QUOD_INT_1"
symbol = "USD/ZAR"
security_type_spo = "FXSPOT"
security_type_fwd = "FXFWD"
settle_date_spo = spo()
settle_date_1w = wk1()
settle_type_spo = "0"
settle_type_w1 = "W1"
qty = "1256324"
currency = "USD"
settle_currency = "ZAR"
side = "1"

expected_pos_client = qty
expected_pos_quod = '676'
expected_pos_client_intern = '-1257000'

expected_pos_client_2 = "2512648"
expected_pos_quod_2 = '352'
expected_pos_client_intern_2 = '-2513000'


def send_rfq_order_spot(params_spot):
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price=price). \
        verify_order_pending(). \
        verify_order_filled()


def send_rfq_order_fwd(params_fwd):
    rfq = FixClientSellRfq(params_fwd)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price=price). \
        verify_order_pending(). \
        verify_order_filled_fwd(price=price)


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


def check_order_book_1(even_name, case_id, base_request, act_ob, qty_exp, status_exp, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(
        ["Order ID", 'AO', "Orig", 'AutoHedger', "Strategy", "Hedging_Test", "Symbol", symbol, "Client ID", client])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(qty_exp), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])

    verifier.verify()
    time.sleep(0.5)
    return response[order_id.name]


def check_order_book_2(even_name, case_id, base_request, act_ob, qty_exp, status_exp, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'MO', "Orig", 'FIX', "Symbol", symbol, "Client ID", client])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(qty_exp), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])

    verifier.verify()
    time.sleep(0.5)
    return response[order_id.name]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    pos_service = Stubs.act_fx_dealing_positions
    case_base_request = get_base_request(session_id, case_id)
    try:
        # Precondition
        initial_pos_cl = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        initial_pos_qv = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        initial_pos_client_intern_ = get_dealing_positions_details(pos_service, case_base_request, symbol,
                                                                   account_client_intern)
        # Step 4
        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        send_rfq_order_spot(params_spot)
        actual_pos_client_ = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        expected_pos_client = str(int(qty) + int(initial_pos_cl))
        compare_position('Checking positions Client AURUM1_1', case_id, expected_pos_client, actual_pos_client_)

        actual_pos_quod_ = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        expected_pos_quod = 676 + int(initial_pos_qv)
        if expected_pos_quod > 1000:
            expected_pos_quod = expected_pos_quod - 1000
        compare_position('Checking positions Quod QUOD4_1', case_id, str(expected_pos_quod), actual_pos_quod_)

        actual_pos_client_intern_ = get_dealing_positions_details(pos_service, case_base_request, symbol,
                                                                  account_client_intern)
        ah_qty = FXOrderBook(case_id, case_base_request).set_filter(
            ["Order ID", "MO", "Orig", "AutoHedger", "Lookup", "USD/ZAR-SPO.SPO", "Client ID", "QUOD4", "InstrType",
             "FXSpot"]).extract_field("Qty").replace(",", "")
        if initial_pos_client_intern_!=0:
            expected_pos_client_intern = int(initial_pos_client_intern_) - int(ah_qty)
            if abs(expected_pos_client_intern) >= 5000000:
                expected_pos_client_intern = expected_pos_client_intern + 5000000

        compare_position('Checking positions Quod QUOD_INT_1', case_id, str(expected_pos_client_intern),
                         actual_pos_client_intern_)

        # Precondition
        initial_pos_cl = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        initial_pos_qv = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        initial_pos_client_intern_ = get_dealing_positions_details(pos_service, case_base_request, symbol,
                                                                   account_client_intern)

        # Step 6
        params_fwd = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                       securitytype=security_type_fwd, settldate=settle_date_1w,
                                       settltype=settle_type_w1, securityid=symbol, settlcurrency=settle_currency,
                                       currency=currency, side=side,
                                       account=account_client)
        send_rfq_order_fwd(params_fwd)
        actual_pos_client_ = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        expected_pos_client = str(int(qty) + int(initial_pos_cl))
        compare_position('Checking positions Client AURUM1_1', case_id, expected_pos_client, actual_pos_client_)
        actual_pos_quod_ = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        expected_pos_quod = 676 + int(initial_pos_qv)
        if expected_pos_quod > 1000:
            expected_pos_quod = expected_pos_quod - 1000
        compare_position('Checking positions Quod QUOD4_1', case_id, str(expected_pos_quod), actual_pos_quod_)
        ah_qty = get_dealing_positions_details(pos_service, case_base_request, symbol,
                                                                  account_client_intern)

        ah_qty = FXOrderBook(case_id, case_base_request).set_filter(
            ["Order ID", "MO", "Orig", "AutoHedger", "Lookup", "USD/ZAR-SPO.SPO", "Client ID", "QUOD4", "InstrType",
             "FXSpot"]).extract_field("Qty").replace(",", "")
        if initial_pos_client_intern_!=0:
            expected_pos_client_intern = int(initial_pos_client_intern_) - int(ah_qty)
            if abs(expected_pos_client_intern) >= 5000000:
                expected_pos_client_intern = expected_pos_client_intern + 5000000

        compare_position('Checking positions Quod QUOD_INT_1', case_id, str(expected_pos_client_intern),
                         actual_pos_client_intern_)


    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
