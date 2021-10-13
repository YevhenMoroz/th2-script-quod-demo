import logging
from pathlib import Path
import time
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from custom.tenor_settlement_date import spo, wk1
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.aggregated_rates_wrappers import PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import get_base_request, call

client = "AURUM1"
account_client = "AURUM1_1"
account_quod = "QUOD4_1"
ah_client = "QUOD4"
account_client_intern = "QUOD_INT_1"
symbol = "EUR/USD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
qty = "3000000"
currency = "EUR"
settle_currency = "USD"
side = "1"
firm_account = "QUOD4"
from_currency = 'EUR'
to_currency = 'USD'
case_tenor = 'Spot'

def create_or_get_esp_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_esp_tile(base_request, service, from_c, to_c, tenor, qty):
    from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    modify_request.set_quantity(qty)
    call(service.modifyRatesTile, modify_request.build())


def place_order_esp(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def send_order(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_place()
    order_ticket.set_client(firm_account)
    order_ticket.set_strategy('Hedging_Test')
    order_ticket.set_tif('GoodTillCancel')
    order_ticket.set_order_type('Market')
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


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


def check_order_book_AO(even_name, case_id, base_request, act_ob, qty_exp, status_exp, client, id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(
        ["Order ID", 'AO', "Orig", 'AutoHedger', "Strategy", "Hedging_Test", "Symbol", symbol, "Client ID", client])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    tif = ExtractionDetail("orderBook.tif", "TIF")
    ord_type = ExtractionDetail("orderBook.ord_type", "OrdType")
    status = ExtractionDetail("orderBook.sts", "Sts")
    exec_pcy = ExtractionDetail("orderBook.exec_pcy", "ExecPcy")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, order_id, tif, ord_type, exec_pcy])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(qty_exp), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])
    verifier.compare_values('TIF', "FillOrKill", response[tif.name])
    verifier.compare_values('OrdType', "Market", response[ord_type.name])
    verifier.compare_values('ExecPcy', "Synth (Quod MultiListing)", response[exec_pcy.name])
    verifier.compare_values('Checking thad id changed', id, response[order_id.name], VerificationMethod.NOT_EQUALS)
    verifier.verify()
    time.sleep(0.5)
    return response[order_id.name]


def check_order_book_MO(even_name, case_id, base_request, act_ob, qty_exp, status_exp, client):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'MO', "Orig", 'AutoHedger', "Symbol", symbol, "Client ID", client])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    tif = ExtractionDetail("orderBook.tif", "TIF")
    ord_type = ExtractionDetail("orderBook.ord_type", "OrdType")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    exec_pcy = ExtractionDetail("orderBook.exec_pcy", "ExecPcy")
    strategy = ExtractionDetail("orderBook.strategy", "Strategy")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, order_id, exec_pcy, tif, ord_type, strategy])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', str(qty_exp), response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])
    verifier.compare_values('TIF', "FillOrKill", response[tif.name])
    verifier.compare_values('OrdType', "Market", response[ord_type.name])
    verifier.compare_values('ExecPcy', "DMA", response[exec_pcy.name])
    verifier.compare_values('Strategy', "", response[strategy.name])

    verifier.verify()
    time.sleep(0.5)
    return response[order_id.name]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    pos_service = Stubs.act_fx_dealing_positions
    case_base_request = get_base_request(session_id, case_id)
    ob_act = Stubs.win_act_order_book
    ar_service = Stubs.win_act_aggregated_rates_service
    order_ticket_service = Stubs.win_act_order_ticket_fx
    base_details = BaseTileDetails(base=case_base_request)
    order_id = ''
    try:
        #Precondition
        # initial_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        # initial_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        #
        # # Step 1
        # params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
        #                                 securitytype=security_type_spo, settldate=settle_date_spo,
        #                                 settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
        #                                 currency=currency, side=side,
        #                                 account=account_client)
        # rfq = FixClientSellRfq(params_spot)
        # rfq.send_request_for_quote()
        # rfq.verify_quote_pending()
        # price = rfq.extract_filed("OfferPx")
        # rfq.send_new_order_single(price=price). \
        #     verify_order_pending(). \
        #     verify_order_filled()
        # time.sleep(5)
        # order_id = check_order_book_AO('Checking placed order AO, triggered by FIX', case_id, case_base_request, ob_act,
        #                     '3000000', "Terminated", ah_client, order_id)
        # actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        # expected_pos_client = str(int(qty)+int(initial_pos_client))
        # compare_position('Checking positions Client AURUM1_1', case_id, expected_pos_client, actual_pos_client)
        # actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        # expected_pos_quod = str(0 + int(initial_pos_quod))
        # compare_position('Checking positions Quod QUOD4_1', case_id, expected_pos_quod, actual_pos_quod)
        #
        # # Step 2-3
        # initial_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        #
        # create_or_get_esp_tile(base_details, ar_service)
        modify_esp_tile(base_details, ar_service, from_currency, to_currency, case_tenor, qty)
        place_order_esp(base_details, ar_service)
        send_order(case_base_request, order_ticket_service)
        # check_order_book_AO('Checking placed order AO, triggered by FIX', case_id, case_base_request, ob_act,
        #                     '3000000', "Terminated", ah_client, order_id)
        # actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        # expected_pos_cl= actual_pos_client
        # compare_position('Checking positions Client AURUM1_1', case_id, expected_pos_cl, actual_pos_client)
        # actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        # expected_pos_qv= str((int(initial_pos_quod)+0))
        # compare_position('Checking positions Quod QUOD4_1', case_id, expected_pos_qv, actual_pos_quod)
        #
        # # PostConditions
        # params_spot = CaseParamsSellRfq(client, case_id, orderqty='3000000', symbol=symbol,
        #                                 securitytype=security_type_spo, settldate=settle_date_spo,
        #                                 settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
        #                                 currency=currency, side='2',
        #                                 account=account_client)
        # rfq = FixClientSellRfq(params_spot)
        # rfq.send_request_for_quote()
        # rfq.verify_quote_pending()
        # price = rfq.extract_filed("BidPx")
        # rfq.send_new_order_single(price=price). \
        #     verify_order_pending(). \
        #     verify_order_filled()
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
