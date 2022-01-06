import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_esp_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_esp_tile(base_request, service, from_c, to_c, tenor, venue):
    from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    from win_gui_modules.aggregated_rates_wrappers import ContextActionRatesTile
    venue_filter = ContextActionRatesTile.create_venue_filter(venue)
    add_agr_rates = ContextActionRatesTile.add_aggregated_rates(details=base_request)
    modify_request.add_context_actions([venue_filter, add_agr_rates])
    call(service.modifyRatesTile, modify_request.build())


def create_or_get_pricing_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_pricing_tile(base_request, service, instrument, client):
    from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def extract_pts_from_esp(base_request, service):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTileAsk.Pts", "Pts"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTileBid.Pts", "Pts"))
    response = call(service.extractESPAggrRatesTableValues, extract_table_request.build())
    bid_pts = float(response["rateTileBid.Pts"])
    ask_pts = float(response["rateTileAsk.Pts"])
    return [bid_pts, ask_pts]


def extract_price_from_pricing_tile(base_request, service):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileValues
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_bid_large_value("rates_tile.bid_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    extract_value_request.extract_bid_pips("rates_tile.bid_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    bid = float(response["rates_tile.bid_large"] + response["rates_tile.bid_pips"])
    ask = float(response["rates_tile.ask_large"] + response["rates_tile.ask_pips"])
    return [bid, ask]


def check_price_on_pricing_tile(case_id, price, spot, pts):

    expected_price = spot + pts / 10000

    verifier = Verifier(case_id)
    verifier.set_event_name("Check price")
    verifier.compare_values("Price", str(round(expected_price, 5)), str(price))
    verifier.verify()


def extract_column_base(base_request, service):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBase", "Base"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBase", "Base"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    bid_base = float(response["rateTile.bidBase"])
    ask_base = float(response["rateTile.askBase"])
    return [bid_base, ask_base]


def extract_column_spot(base_request, service):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askSpot", "Spot"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidSpot", "Spot"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    bid_spot = float(response["rateTile.bidSpot"])
    ask_spot = float(response["rateTile.askSpot"])
    return [bid_spot, ask_spot]


def check_column_pts(base_request, service, case_id, bid_pts, ask_pts, bid_base, ask_base):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askPts", "Pts"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidPts", "Pts"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    bid_pts_mm = float(response["rateTile.bidPts"])
    ask_pts_mm = float(response["rateTile.askPts"])

    expected_bid_pts = bid_pts - bid_base
    expected_ask_pts = ask_pts + ask_base

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Pts in Pricing tile")
    verifier.compare_values("Bid pts", str(expected_bid_pts), str(bid_pts_mm))
    verifier.compare_values("Ask pts", str(expected_ask_pts), str(ask_pts_mm))
    verifier.verify()

    return [bid_pts_mm, ask_pts_mm]


def check_ask_price(case_id, esp_bid, pricing_price, base):
    expected_price = esp_bid + base / 10000
    verifier = Verifier(case_id)
    verifier.set_event_name("Check ask price on Pricing tile")
    verifier.compare_values("ask price", str(round(expected_price, 5)), str(pricing_price))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    from_curr = "GBP"
    to_curr = "AUD"
    tenor = "1W"
    venue = "HSB"
    instrument = "GBP/AUD-1W"
    client_tier = "Silver"

    def_md_symbol_gbp_aud_fwd = "GBP/AUD:FXF:WK1:HSBC"
    def_md_symbol_gbp_aud_spo = "GBP/AUD:SPO:REG:HSBC"
    symbol_gbp_aud = "GBP/AUD"

    try:
        # Step 1
        create_or_get_esp_tile(base_details, ar_service)
        modify_esp_tile(base_details, ar_service, from_curr, to_curr, tenor, venue)
        # Step 2
        create_or_get_pricing_tile(base_details, cp_service)
        modify_pricing_tile(base_details, cp_service, instrument, client_tier)
        # Step 3
        # FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_gbp_aud_spo, symbol_gbp_aud)).send_market_data_spot()
        esp_pts = extract_pts_from_esp(base_details, ar_service)
        mm_base = extract_column_base(base_details, cp_service)
        pts_mm = check_column_pts(base_details, cp_service, case_id, esp_pts[0], esp_pts[1],
                                  mm_base[0], mm_base[1])
        spot_mm = extract_column_spot(base_details, cp_service)
        price_mm = extract_price_from_pricing_tile(base_details, cp_service)

        check_price_on_pricing_tile(case_id, price_mm[0], spot_mm[0], pts_mm[0])
        check_price_on_pricing_tile(case_id, price_mm[1], spot_mm[1], pts_mm[1])

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tiles
            call(ar_service.closeRatesTile, base_details.build())
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
