from datetime import datetime

from custom.tenor_settlement_date import spo
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ClientRFQTileOrderDetails, \
    ModifyClientRFQTileRequest, SelectRowsRequest
import logging
from pathlib import Path
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
instrument_spot = 'EUR/JPY-Spot'
instrument_forward = 'EUR/JPY-1W'
tier = "Iridium1"
near_tenor = "Spot"
far_tenor = "1W"
from_curr = "EUR"
to_curr = "JPY"
client_tier = "Iridium1"
client = "Iridium1"
qty = "300000000"
symbol = "EUR/JPY"
security_type = "FXSPOT"
owner = Stubs.custom_config['qf_trading_fe_user']
simulator = Stubs.simulator
act = Stubs.fix_act
default_md_symbol_spo = "EUR/JPY:SPO:REG:CITI"
no_md_entries_eur_jpy_citi = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 104.630,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 104.640,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 104.620,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 104.650,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 104.610,
        "MDEntrySize": 10000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 104.660,
        "MDEntrySize": 10000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 104.600,
        "MDEntrySize": 300000000,
        "MDEntryPositionNo": 4,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 104.670,
        "MDEntrySize": 300000000,
        "MDEntryPositionNo": 4,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    }
]


def create_or_get_pricing_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def press_executable(details, service):
    modify_request = ModifyRatesTileRequest(details=details)
    modify_request.press_pricing()
    call(service.modifyRatesTile, modify_request.build())


def select_rows(base_tile_details, row_numbers, cp_service):
    request = SelectRowsRequest(base_tile_details)
    request.set_row_numbers(row_numbers)
    call(cp_service.selectRows, request.build())


def create_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.createClientRFQTile, base_tile_data)


def close_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.closeClientRFQTile, base_tile_data)


def modify_client_rfq_tile(cp_service, base_tile_data):
    request = ModifyClientRFQTileRequest(data=base_tile_data)
    request.change_client_tier(client_tier)
    request.set_from_curr(from_curr)
    request.set_to_curr(to_curr)
    request.change_near_tenor(near_tenor)
    request.change_far_tenor(far_tenor)
    request.change_near_leg_aty(qty)
    request.change_client(client)
    call(cp_service.modifyRFQTile, request.build())


def place_client_rfq_order(cp_service, base_tile_data):
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    requests.set_action_sell()
    call(cp_service.placeClientRFQOrder, requests.build())


def send_client_rfq(cp_service, base_tile_data):
    call(cp_service.sendRFQOrder, base_tile_data)


def check_quote_request_b(base_request, service, case_id,
                          status="Terminated", venue="QUODFX", quote_status='Filled'):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_filter(["Venue", venue, "User", owner, 'Status', status, 'Qty', qty])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Venue', venue, response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values('QuoteStatus', quote_status, response[qrb_quote_status.name])
    verifier.verify()


def check_order_book(base_request, act_ob, venue='QUODFX', sts='Terminated'):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(['Venue', venue, 'Owner', owner, 'Qty', qty])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    order_sts = ExtractionDetail('orderBook.Sts', 'Sts')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id, order_sts])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier()
    verifier.set_event_name('Checking that order executed')
    verifier.compare_values('Status', sts, response[order_sts.name])
    verifier.compare_values('ID', response[order_id.name], response[order_id.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    details_tile_spot = BaseTileDetails(base=case_base_request, window_index=0)
    details_tile_forward = BaseTileDetails(base=case_base_request, window_index=1)
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service
    try:
        # Preconditions
        create_or_get_pricing_tile(details_tile_spot, cp_service)
        create_or_get_pricing_tile(details_tile_forward, cp_service)
        modify_rates_tile(details_tile_spot, cp_service, instrument_spot, tier)
        modify_rates_tile(details_tile_forward, cp_service, instrument_forward, tier)
        FixClientBuy(CaseParamsBuy(case_id, default_md_symbol_spo, symbol, security_type)). \
            send_market_data_spot('Custom Market Data from BUY SIDE USD/JPY')

        FixClientBuy(CaseParamsBuy(case_id, default_md_symbol_spo, symbol, security_type).
                     prepare_custom_md_spot(no_md_entries_eur_jpy_citi)).send_market_data_spot()
        select_rows(details_tile_spot, [4], cp_service)
        press_executable(details_tile_spot, cp_service)
        select_rows(details_tile_forward, [1, 2, 3], cp_service)
        press_executable(details_tile_forward, cp_service)
        call(cp_service.closeRatesTile, details_tile_spot.build())
        call(cp_service.closeRatesTile, details_tile_forward.build())
        create_client_rfq_tile(cp_service, base_tile_data)
        modify_client_rfq_tile(cp_service, base_tile_data)
        send_client_rfq(cp_service, base_tile_data)
        place_client_rfq_order(cp_service, base_tile_data)
        check_quote_request_b(case_base_request, ar_service, case_id)
        check_order_book(case_base_request, ob_act)
    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            close_client_rfq_tile(cp_service, base_tile_data)
            create_or_get_pricing_tile(details_tile_spot, cp_service)
            create_or_get_pricing_tile(details_tile_forward, cp_service)
            modify_rates_tile(details_tile_spot, cp_service, instrument_spot, tier)
            modify_rates_tile(details_tile_forward, cp_service, instrument_forward, tier)
            select_rows(details_tile_spot, [4], cp_service)
            press_executable(details_tile_spot, cp_service)
            select_rows(details_tile_forward, [1, 2, 3], cp_service)
            press_executable(details_tile_forward, cp_service)
            call(cp_service.closeRatesTile, details_tile_spot.build())
            call(cp_service.closeRatesTile, details_tile_forward.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
