import logging
import random
import time
from datetime import datetime

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from custom.tenor_settlement_date import wk1, spo
from stubs import Stubs
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.win_gui_wrappers.data_set import OrderBookColumns, TimeInForce, ExecSts
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX
from win_gui_modules.client_pricing_wrappers import PlaceRateTileTableOrderRequest, PlaceRatesTileOrderRequest, \
    RatesTileTableOrdSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request

alias_fh = "fix-fh-314-luna"

symbol = 'USD/PHP'
security_type = 'NDF'
tenor = 'WK1'
tenor_fe = '1W'
tenor_fe_spo = 'Spot'
venue = 'HSBC'

BUY = RatesTileTableOrdSide.BUY
instrument = f'{symbol}-{tenor_fe}'
instrument_spot = f'{symbol}-{tenor_fe_spo}'
client_tier = 'Palladium1'
default_md_symbol_fwd_hsbc = f'{symbol}:{security_type}:{tenor}:{venue}'
print(default_md_symbol_fwd_hsbc)
md_instrument = {
    'Instrument': {
        'Symbol': 'USD/PHP',
        'SecurityType': 'FXNDF'
    }
}
qty = str(random.randint(1000000,2000000))
no_md_entries_fwd_hsbc = [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18039,
                    "MDEntrySize": 1000000,
                    "MDEntrySpotRate": 1.18038,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18051,
                    "MDEntrySize": 1000000,
                    "MDEntrySpotRate": 1.18052,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18031,
                    "MDEntrySize": 5000000,
                    "MDEntrySpotRate": 1.18032,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 0,
                    'SettlDate': wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18067,
                    "MDEntrySize": 5000000,
                    "MDEntrySpotRate": 1.18068,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 2,
                    "MDQuoteType": 0,
                    'SettlDate': wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18029,
                    "MDEntrySize": 9000000,
                    "MDEntrySpotRate": 1.18040,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 0,
                    'SettlDate': wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18087,
                    "MDEntrySize": 9000000,
                    "MDEntrySpotRate": 1.18088,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 3,
                    "MDQuoteType": 0,
                    'SettlDate': wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]


def open_ot_by_doubleclick_row(btd, cp_service, _row, _side):
    request = PlaceRateTileTableOrderRequest(btd, _row, _side)
    call(cp_service.placeRateTileTableOrder, request.build())


def place_order(base_request, service):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_client(client_tier)
    place_request.set_quantity(qty)
    call(service.placeRatesTileOrder, place_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    fix_manager_fh = FixManager(alias_fh, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_details = BaseTileDetails(base=case_base_request)
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    ob_names = OrderBookColumns
    sts_names = ExecSts
    try:
        # Send market data to the HSBC venue USD/PHP FWD non executable
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX().set_market_data().\
            update_repeating_group('NoMDEntries', no_md_entries_fwd_hsbc). \
            change_parameters(md_instrument). \
            update_MDReqID(default_md_symbol_fwd_hsbc, alias_fh, 'FX')

        #
        fix_manager_fh.send_message(market_data_snap_shot, "Send MD HSBC USD/PHP Non Executable")
        time.sleep(5)
        #
        rates_tile = ClientRatesTile(case_id, session_id)
        rates_tile.modify_client_tile(instrument=instrument, client_tier=client_tier)
        open_ot_by_doubleclick_row(base_tile_data, cp_service, 1, BUY)
        place_order(base_details, cp_service)

        FXOrderBook(case_id, session_id).check_order_fields_list({
            ob_names.qty.value: qty,
            ob_names.sts.value: sts_names.rejected.value,
            ob_names.free_notes: 'empty book'},
            event_name='Checking that order rejected')

        rates_tile = ClientRatesTile(case_id, session_id)
        rates_tile.modify_client_tile(instrument=instrument_spot, client_tier=client_tier)
        open_ot_by_doubleclick_row(base_tile_data, cp_service, 1, BUY)
        place_order(base_details, cp_service)

        FXOrderBook(case_id, session_id).check_order_fields_list({
            ob_names.qty.value: qty,
            ob_names.sts.value: sts_names.terminated.value},
            event_name='Checking that order rejected')

        # Changing MD to executable
        for i in no_md_entries_fwd_hsbc:
            i["MDQuoteType"] = 1

        # Send market data to the HSBC venue USD/PHP FWD executable
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshBuyFX().set_market_data() \
            .update_repeating_group('NoMDEntries', no_md_entries_fwd_hsbc). \
            update_MDReqID(default_md_symbol_fwd_hsbc, alias_fh, 'FX')
        fix_manager_fh.send_message(market_data_snap_shot, "Send MD HSBC USD/PHP Executable")
        time.sleep(5)
        rates_tile.close_tile()
    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)