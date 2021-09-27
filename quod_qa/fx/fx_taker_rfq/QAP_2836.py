import logging
import random
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, near_qty, cur1, cur2, near_tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service, side):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(side)
    call(service.placeRFQOrder, rfq_request.build())


def check_order_book(base_request, act_ob, case_id, symbol, qty, client, account):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(['Symbol', symbol, 'Qty', qty])
    ob_orig = ExtractionDetail("orderBook.Orig", "Orig")
    ob_client = ExtractionDetail("orderBook.Client", "Client ID")
    ob_account = ExtractionDetail("orderBook.Account", "Account ID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_orig,
                                                                                 ob_client,
                                                                                 ob_account])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('Order origin', 'TradingFE', response[ob_orig.name])
    verifier.compare_values('Order Account ID', account, response[ob_account.name])
    verifier.compare_values('Order Client ID', client, response[ob_client.name])
    verifier.verify()


def extract_positions(del_act, base_request, symbol, account):
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
    return response["dealingpositions.position"].replace(",", "")


def check_positions(act_pos, exp_pos, case_id, method, name):
    verifier = Verifier(case_id)
    verifier.set_event_name(name)
    verifier.compare_values('Positions', exp_pos, act_pos, method)
    verifier.verify()

def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    pos_act = Stubs.act_fx_dealing_positions

    case_name = Path(__file__).name[:-3]
    case_client = "QUOD"
    case_account = "QUOD_1"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    symbol = "EUR/USD"
    case_tenor = "Spot"
    case_qty = random.randint(1000000, 5000000)
    side_buy = RFQTileOrderSide.BUY
    side_sell = RFQTileOrderSide.SELL
    verificaion_equal = VerificationMethod.EQUALS
    verificaion_not_equal = VerificationMethod.NOT_EQUALS
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        initial_pos = extract_positions(pos_act, case_base_request, symbol, case_account)
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                        case_tenor, case_client)
        send_rfq(base_rfq_details, ar_service)
        place_order_tob(base_rfq_details, ar_service, side_buy)
        check_order_book(case_base_request, ob_act, case_id, symbol, str(case_qty), case_client, case_account)
        # Step 3
        affected_pos = extract_positions(pos_act, case_base_request, symbol, case_account)
        check_positions(affected_pos, initial_pos, case_id, verificaion_not_equal, 'Checking that positions changed')
        send_rfq(base_rfq_details, ar_service)
        place_order_tob(base_rfq_details, ar_service, side_sell)
        affected_pos = extract_positions(pos_act, case_base_request, symbol, case_account)
        check_positions(affected_pos, initial_pos, case_id, verificaion_equal,
                        'Checking that positions back to initial')
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
