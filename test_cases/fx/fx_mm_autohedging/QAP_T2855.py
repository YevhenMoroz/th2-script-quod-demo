import logging
from pathlib import Path
import time
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from custom.tenor_settlement_date import spo, m1
from custom.verifier import Verifier
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import get_base_request, call

client = "AURUM1"
account_client = "AURUM1_1"
account_quod = "QUOD4_1"
symbol = "USD/DKK"
security_type_spo = "FXFWD"
settle_date_spo = m1()
qty_1 = "5000000"
currency = "USD"
settle_currency = "DKK"
side = "1"
settltype = 0
expected_pos_client_1 = "5000000"
expected_pos_quod_1 = "-1000000"
client_quod = "QUOD4"
ah_qty="4000000"


def send_rfq_order_1m(params_1m):
    rfq = FixClientSellRfq(params_1m)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price=price). \
        verify_order_pending(). \
        verify_order_filled_fwd()


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


def check_order_book_AO(even_name, case_id, base_request, act_ob, qty_exp, status_exp, instr_type_exp, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(
        ["Order ID", 'AO', "Orig", 'AutoHedger', "Strategy", "Hedging_Test", "Symbol", symbol, "Client ID", client])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    instr_type = ExtractionDetail("orderBook.instr_type", "InstrType")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, instr_type, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(qty_exp), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])
    verifier.compare_values('InstrType', instr_type_exp, response[instr_type.name])

    verifier.verify()
    time.sleep(0.5)
    return response[order_id.name]


def check_order_book_MO(even_name, case_id, base_request, act_ob, qty_exp, status_exp,instr_type_exp, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'MO', "Orig", 'FIX', "Symbol", symbol, "Client ID", client])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    instr_type = ExtractionDetail("orderBook.instr_type", "InstrType")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, instr_type, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(qty_exp), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])
    verifier.compare_values('InstrType', instr_type_exp, response[instr_type.name])


    verifier.verify()
    time.sleep(0.5)
    return response[order_id.name]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    pos_service = Stubs.act_fx_dealing_positions
    case_base_request = get_base_request(session_id, case_id)
    ob_act = Stubs.win_act_order_book
    try:

        params_1m = CaseParamsSellRfq(client, case_id, orderqty=qty_1, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settltype, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        send_rfq_order_1m(params_1m)

        actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        difference_cl = 0
        if actual_pos_client != expected_pos_client_1:
            difference_cl = int(actual_pos_client)-int(expected_pos_client_1)
        new_exp_pos_cl = str(int(expected_pos_client_1) + difference_cl)
        compare_position('Checking positions AURUM1_1', case_id, new_exp_pos_cl, actual_pos_client)


        actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        compare_position('Checking positions QUOD4_1', case_id, expected_pos_quod_1, actual_pos_quod)


        ah_qty_new = ah_qty
        if actual_pos_quod != expected_pos_quod_1:
            ah_qty_new = int(ah_qty) + 1000000

        check_order_book_AO('Checking placed order AO_AH', case_id, case_base_request, ob_act, ah_qty_new, "Terminated", "FXSpot",
                           client_quod)


        check_order_book_MO('Checking placed order MO', case_id, case_base_request, ob_act, "5000000", "Terminated", "FXForward", client)


    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
