import time

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ModifyRatesTileRequest as ModifyMM
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest as ModifyESP, ContextActionRatesTile, \
    ExtractRatesTileDataRequest, ActionsRatesTile
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, DeselectRowsRequest

api = Stubs.api_service

md_entry = [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19500,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19500,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19450,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19600,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19400,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19700,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19350,
                    "MDEntrySize": 13000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19800,
                    "MDEntrySize": 13000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]

def_md_symbol_eur_gbp = "EUR/GBP:SPO:REG:HSBC"
symbol_eur_gbp = "EUR/GBP"
core_spot_strategy_vwap = 'VWP'
core_spot_strategy_direct = 'DIR'
from_currency = 'EUR'
to_currency = 'GBP'
tenor = 'Spot'
instrument = 'EUR/GBP-Spot'
client_tier = 'Palladium2'
venue = 'HSB'
rows_default = 3
rows_with_new_md = 4
ask_pts_exp = 700
bid_pts_exp = 400
unconfigured_ask_pts_exp = 800
unconfigured_bid_pts_exp = 350

def set_core_strategy_for_tier(case_id, core_strategy):
    modify_params = {
        "alive": "true",
        "clientTierID": 2000011,
        "clientTierName": "Palladium2",
        "enableSchedule": "false",
        "pricingMethod": core_strategy
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyClientTier', modify_params, 'rest_wa314luna'),
                                     parent_event_id=case_id))


def modify_cp_rates_tile(base_request, service, instr, client):
    modify_request = ModifyMM(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instr)
    call(service.modifyRatesTile, modify_request.build())


def modify_agg_rates_tile(base_request, service, from_c, to_c, ten):
    modify_request = ModifyESP(details=base_request)
    modify_request.set_instrument(from_c, to_c, ten)
    call(service.modifyRatesTile, modify_request.build())


def open_direct_venue(base_request, service, ven):
    modify_request = ModifyESP(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filter(ven)
    add_dve_action = ContextActionRatesTile.open_direct_venue_panel()
    modify_request.add_context_actions([venue_filter, add_dve_action])
    call(service.modifyRatesTile, modify_request.build())


def add_venue_rows(base_request, service, ven):
    modify_request = ModifyESP(details=base_request)
    add_row = ActionsRatesTile().click_to_direct_venue_add_raw(ven)
    modify_request.add_actions([add_row, add_row, add_row, add_row, add_row])
    call(service.modifyRatesTile, modify_request.build())


def extract_pts_and_band(base_request, service, rows: int):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(rows)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidBase", "Base"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askBase", "Base"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bidPx", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("askPx", "Px"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    deselect_rows_request = DeselectRowsRequest(details=base_request)
    call(service.deselectRows, deselect_rows_request.build())
    return [response['askPx'], response['bidPx'], response['bidBase']]


def check_pts_default(case_id, ask_exp, bid_exp, ask_act, bid_act, base):
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking pts')
    verifier.compare_values('ask', str(int(ask_exp)+int(float(base)*10)), ask_act)
    verifier.compare_values('bid', str(int(bid_exp)-int(float(base)*10)), bid_act)
    verifier.verify()


def check_pts_with_new_md(case_id, ask_exp, bid_exp, ask_act, bid_act, base):
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking pts with new band')
    verifier.compare_values('ask', str(ask_exp), str(ask_act))
    verifier.compare_values('bid', str(bid_exp), str(bid_act))
    verifier.compare_values('Base', '', base)
    verifier.verify()


def execute(report_id, session_id):
    #
    # TODO: Add extraction from Taker ESP tile
    #
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_details = BaseTileDetails(base=case_base_request)
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service
    pos_service = Stubs.act_fx_dealing_positions
    try:
        call(cp_service.createRatesTile, base_details.build())
        call(ar_service.createRatesTile, base_details.build())

        set_core_strategy_for_tier(case_id, core_spot_strategy_direct)
        modify_cp_rates_tile(base_details, cp_service, instrument, client_tier)
        modify_agg_rates_tile(base_details, ar_service, from_currency, to_currency, tenor)
        open_direct_venue(base_details, ar_service, venue)
        add_venue_rows(base_details, ar_service, venue)

        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_eur_gbp, symbol_eur_gbp).prepare_custom_md_spot(
            md_entry[:6])).send_market_data_spot()
        result = extract_pts_and_band(base_details, cp_service, rows_default)
        check_pts_default(case_id, ask_pts_exp, bid_pts_exp, result[0], result[1], result[2])

        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_eur_gbp, symbol_eur_gbp).prepare_custom_md_spot(
            md_entry)).send_market_data_spot()
        result = extract_pts_and_band(base_details, cp_service, rows_with_new_md)
        check_pts_with_new_md(case_id, unconfigured_ask_pts_exp, unconfigured_bid_pts_exp, result[0], result[1], result[2])

    except Exception as ex:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
            call(ar_service.closeRatesTile, base_details.build())
            # Set default parameters
            set_core_strategy_for_tier(case_id, core_spot_strategy_vwap)
            FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_eur_gbp, symbol_eur_gbp).prepare_custom_md_spot(
                md_entry[:6])).send_market_data_spot()
        except Exception:
            logging.error("Error execution", exc_info=True)
