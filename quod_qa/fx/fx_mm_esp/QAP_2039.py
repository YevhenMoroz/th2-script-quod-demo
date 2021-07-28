import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, ModifyRatesTileRequest
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
    modify_request.add_context_actions([venue_filter])
    call(service.modifyRatesTile, modify_request.build())


def create_or_get_pricing_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def modify_pricing_tile(base_request, service, instrument, client):
    from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def extract_price_from_esp(base_request, service):
    from win_gui_modules.aggregated_rates_wrappers import ExtractRatesTileDataRequest
    extraction_value = ExtractRatesTileDataRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_value.set_extraction_id(extraction_id)
    extraction_value.extract_best_bid("ratesTile.Bid")
    extraction_value.extract_best_ask("ratesTile.Ask")
    response = call(service.extractRatesTileValues, extraction_value.build())
    bid = float(response["ratesTile.Bid"])
    ask = float(response["ratesTile.Ask"])
    return [bid, ask]


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


def extract_column_base(base_request, service):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBase", "Base (b)"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBase", "Base (b)"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    bid_base = float(response["rateTile.bidBase"])
    ask_base = float(response["rateTile.askBase"])
    return [bid_base, ask_base]


def check_bid_price(case_id, esp_bid, pricing_price, base):
    expected_price = esp_bid * (1 - base / 10000)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check bid price on Pricing tile")
    verifier.compare_values("Bid price", str(round(expected_price, 5)), str(pricing_price))
    verifier.verify()


def check_ask_price(case_id, esp_bid, pricing_price, base):
    expected_price = esp_bid * (1 + base / 10000)
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

    from_curr = "AUD"
    to_curr = "CAD"
    tenor = "Spot"
    venue = "HSB"
    instrument = "AUD/CAD-Spot"
    client_tier = "Silver"

    def_md_symbol_aud_cad = "AUD/CAD:SPO:REG:HSBC"
    symbol_aud_cad = "AUD/CAD"

    try:
        # Step 1
        create_or_get_esp_tile(base_details, ar_service)
        modify_esp_tile(base_details, ar_service, from_curr, to_curr, tenor, venue)
        # Step 2
        create_or_get_pricing_tile(base_details, cp_service)
        modify_pricing_tile(base_details, cp_service, instrument, client_tier)
        # Step 3
        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_aud_cad, symbol_aud_cad)).send_market_data_spot()
        esp_price = extract_price_from_esp(base_details, ar_service)
        pricing_tile_price = extract_price_from_pricing_tile(base_details, cp_service)
        base = extract_column_base(base_details, cp_service)
        check_bid_price(case_id, esp_price[0], pricing_tile_price[0], base[0])
        check_ask_price(case_id, esp_price[1], pricing_tile_price[1], base[1])

        use_default(base_details, cp_service)

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
