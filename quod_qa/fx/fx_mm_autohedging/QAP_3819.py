import logging
import random
from pathlib import Path
import time
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom.verifier import Verifier
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.client_pricing_wrappers import ClientRFQTileOrderDetails, ModifyClientRFQTileRequest
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    ModificationRequest
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import get_base_request, call

client_tier = "AURUM"
client = "AURUM1"
account_client = "AURUM1_1"
account_quod = "QUOD4_1"
account_holder = "CLIENT1_1"
symbol = "EUR/USD"
tenor = 'Spot'
qty = str(random.randint(7000000, 10000000))
currency = "EUR"
settle_currency = "USD"
# Need a user with configured Holder
user = Stubs.custom_config['qf_trading_fe_user']
status_true = True
status_false = False
pos_zero = '0'
expected_pos_client = qty
expected_pos_quod = '0'
expected_pos_client_intern = f'-{qty}'


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


def check_dealer_intervention(base_request, service, case_id, qty):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_list(["Qty", qty, "User", user, 'InstrSymbol', symbol])
    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_id = bca.client_orderid(8)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.status", "Status"))

    response = call(service.getUnassignedRFQDetails, extraction_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check quote request in DI")
    verifier.compare_values("Status", "New", response["dealerIntervention.status"])


def assign_firs_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.assignToMe, base_data.build())


def estimate_first_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.estimate, base_data.build())


def set_hedge_and_send_quote(base_request, service, status):
    modify_request = ModificationRequest(base=base_request)
    modify_request.click_is_hedged_chec_box(status)
    modify_request.send()
    call(service.modifyAssignedRFQ, modify_request.build())


def reject_quote(base_request, service):
    modify_request = ModificationRequest(base=base_request)
    modify_request.reject()
    call(service.modifyAssignedRFQ, modify_request.build())


def create_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.createClientRFQTile, base_tile_data)


def close_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.closeClientRFQTile, base_tile_data)


def modify_client_rfq_tile(cp_service, base_tile_data):
    request = ModifyClientRFQTileRequest(data=base_tile_data)
    request.change_client_tier(client_tier)
    request.set_from_curr(currency)
    request.set_to_curr(settle_currency)
    request.change_near_tenor(tenor)
    request.change_near_leg_aty(qty)
    request.change_client(client)
    call(cp_service.modifyRFQTile, request.build())


def place_client_rfq_order_sell(cp_service, base_tile_data):
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    requests.set_action_sell()
    call(cp_service.placeClientRFQOrder, requests.build())


def place_client_rfq_order_buy(cp_service, base_tile_data):
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    requests.set_action_buy()
    call(cp_service.placeClientRFQOrder, requests.build())


def send_client_rfq(cp_service, base_tile_data):
    call(cp_service.sendRFQOrder, base_tile_data)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)

    pos_service = Stubs.act_fx_dealing_positions
    case_base_request = get_base_request(session_id, case_id)
    dealer_service = Stubs.win_act_dealer_intervention_service
    cp_service = Stubs.win_act_cp_service
    try:
        # Step 1
        create_client_rfq_tile(cp_service, base_tile_data)
        modify_client_rfq_tile(cp_service, base_tile_data)
        send_client_rfq(cp_service, base_tile_data)
        check_dealer_intervention(case_base_request, dealer_service, case_id, qty)
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        set_hedge_and_send_quote(case_base_request, dealer_service, status_false)
        place_client_rfq_order_buy(cp_service, base_tile_data)
        # Step 2
        actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        compare_position('Checking positions Client AURUM1_1', case_id, expected_pos_client, actual_pos_client)
        actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        compare_position('Checking positions Quod QUOD4_1', case_id, expected_pos_quod, actual_pos_quod)
        actual_pos_client_holder = get_dealing_positions_details(pos_service, case_base_request, symbol, account_holder)
        compare_position('Checking positions Quod CLIENT1_1', case_id, expected_pos_client_intern, actual_pos_client_holder)
        # Step 3
        send_client_rfq(cp_service, base_tile_data)
        check_dealer_intervention(case_base_request, dealer_service, case_id, qty)
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        set_hedge_and_send_quote(case_base_request, dealer_service, status_false)
        place_client_rfq_order_sell(cp_service, base_tile_data)
        # Step 4
        actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        compare_position('Checking positions Client AURUM1_1', case_id, pos_zero, actual_pos_client)
        actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        compare_position('Checking positions Quod QUOD4_1', case_id, pos_zero, actual_pos_quod)
        actual_pos_client_holder = get_dealing_positions_details(pos_service, case_base_request, symbol, account_holder)
        compare_position('Checking positions Quod CLIENT1_1', case_id, pos_zero, actual_pos_client_holder)
        # Step 5
        send_client_rfq(cp_service, base_tile_data)
        check_dealer_intervention(case_base_request, dealer_service, case_id, qty)
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        set_hedge_and_send_quote(case_base_request, dealer_service, status_true)
        reject_quote(case_base_request, dealer_service)
        close_client_rfq_tile(cp_service, base_tile_data)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
