import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    modify_request.set_pips(pips)
    call(service.modifyRatesTile, modify_request.build())


def check_spread(base_request, service, case_id):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_spread("rates_tile.spread")
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_bid_large_value("rates_tile.bid_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    extract_value_request.extract_bid_pips("rates_tile.bid_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())

    bid = float(response["rates_tile.bid_large"] + response["rates_tile.bid_pips"])
    ask = float(response["rates_tile.ask_large"] + response["rates_tile.ask_pips"])
    extracted_spread = response["rates_tile.spread"]
    calculated_spread = round((ask - bid) * 10000, 1)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check calculation of spread")
    verifier.compare_values("Spread", str(calculated_spread), extracted_spread)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "EUR/USD-Spot"
    client_tier = "Silver"
    pips = "2"

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier, pips)
        check_spread(base_details, cp_service, case_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
