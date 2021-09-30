import logging
from datetime import datetime
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.order_ticket import ExtractFxOrderTicketValuesRequest, FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd



md_entry = [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19655,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19979,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18900,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19989,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18400,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19998,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]


def create_or_get_esp_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_esp_tile(base_request, service, from_c, to_c, tenor, venue, qty):
    from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    modify_request.set_quantity(qty)
    from win_gui_modules.aggregated_rates_wrappers import ContextActionRatesTile
    venue_filter = ContextActionRatesTile.create_venue_filter(venue)
    modify_request.add_context_actions([venue_filter])
    call(service.modifyRatesTile, modify_request.build())


def open_aggregated_rates(base_request, service):
    from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    from win_gui_modules.aggregated_rates_wrappers import ContextActionRatesTile
    add_agr_rates = ContextActionRatesTile.add_aggregated_rates(details=base_request)
    modify_request.add_context_actions([add_agr_rates])
    call(service.modifyRatesTile, modify_request.build())


def modify_pricing_tile(base_request, service, instrument, client):
    from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def extract_aggr_rates_table_data(service, base_request):
    i = 1
    sum_qty = 0
    price = ''
    while i <= 2:
        extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
        extraction_id = bca.client_orderid(4)
        extract_table_request.set_extraction_id(extraction_id)
        extract_table_request.set_row_number(i)
        extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Px", "Px"))
        extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Qty", "Qty"))
        extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Px", "Px"))
        extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Qty", "Qty"))
        result = call(service.extractESPAggrRatesTableValues, extract_table_request.build())
        sum_qty += int(result["rateTileBid.Qty"].replace('M', '000000'))
        price = result["rateTileBid.Px"]
        i += 1
    return sum_qty, price


def extract_order_ticket_values(base_tile_details, order_ticket_service):
    request = ExtractFxOrderTicketValuesRequest(base_tile_details)
    request.get_price_large('price_large')
    request.get_price_pips('price_pips')
    result = call(order_ticket_service.extractFxOrderTicketValues, request.build())
    return result['price_large']+result['price_pips']


def close_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_close()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def place_esp_by_tob_sell(base_request):
    service = Stubs.win_act_aggregated_rates_service
    btd = BaseTileDetails(base=base_request)
    rfq_request = PlaceESPOrder(details=btd)
    rfq_request.set_action(ESPTileOrderSide.SELL)
    rfq_request.top_of_book()
    call(service.placeESPOrder, rfq_request.build())


def check_prices(case_id, price_exp, price_act_tile, price_act_ot, name):
    verifier = Verifier(case_id)
    verifier.set_event_name(name)
    verifier.compare_values('Checking price on tile', price_exp, price_act_tile)
    verifier.compare_values('Checking price in ot', price_exp, price_act_ot)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    ot_service = Stubs.win_act_order_ticket_fx

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    venue = "HSB"
    qty_7m = '7000000'
    qty_8m = '8000000'
    def_md_symbol_eur_usd = "EUR/USD:SPO:REG:HSBC"
    symbol_eur_usd = "EUR/USD"
    price_exp_6m = '1.18900'
    price_exp_7m = '1.18400'

    try:
        #
        # TODO: Fix extraction/
        #       Add strategies step
        #
        # Precondition
        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_eur_usd, symbol_eur_usd).prepare_custom_md_spot(
            md_entry)).send_market_data_spot()
        # Step 1
        create_or_get_esp_tile(base_details, ar_service)
        modify_esp_tile(base_details, ar_service, from_curr, to_curr, tenor, venue, qty_7m)
        open_aggregated_rates(base_details, ar_service)
        # Step 2
        qty, price_tile = extract_aggr_rates_table_data(ar_service, base_details)
        place_esp_by_tob_sell(case_base_request)
        price_ot = extract_order_ticket_values(base_tile_data, ot_service)
        close_order_ticket(case_base_request, ot_service)
        check_prices(case_id, price_exp_6m, price_tile, price_ot, 'Checking price for 7M')
        # Step 3
        modify_esp_tile(base_details, ar_service, from_curr, to_curr, tenor, venue, qty_8m)
        qty, price_tile = extract_aggr_rates_table_data(ar_service, base_details)
        place_esp_by_tob_sell(case_base_request)
        price_ot = extract_order_ticket_values(base_tile_data, ot_service)
        check_prices(case_id, price_exp_7m, price_tile, price_ot, 'Checking price for 8M')
        close_order_ticket(case_base_request, ot_service)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            pass
            # Close tiles
            call(ar_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
