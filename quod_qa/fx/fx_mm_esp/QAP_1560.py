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


def modify_rates_tile(base_request, service, instrument, client_tier):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client_tier)
    call(service.modifyRatesTile, modify_request.build())


def modify_spread(base_request, service, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_pips(pips)
    modify_request.skew_towards_ask()
    call(service.modifyRatesTile, modify_request.build())


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def check_ask(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask = float(response["rates_tile.ask_large"] + response["rates_tile.ask_pips"])
    return float(ask)


def compare_prices(case_id, ask_before, ask_after, pips):
    pips = float(pips) / 10000
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices")
    verifier.compare_values("Price ask", str(ask_before + pips), str(ask_after))
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "EUR/USD-Spot"
    client_tier = "Silver"
    pips = "20"

    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        # Step 2
        ask_before = check_ask(base_details, cp_service)
        modify_spread(base_details, cp_service, pips)
        ask_after = check_ask(base_details, cp_service)
        # Step 3
        compare_prices(case_id, ask_before, ask_after, pips)
        # Step 4
        use_default(base_details, cp_service)
        ask_after_default = check_ask(base_details, cp_service)
        compare_prices(case_id, ask_before, ask_after_default, "0")

    except Exception:
        logging.error("Error execution", exc_info=True)
    # finally:
    #     try:
    #         # Close tile
    #         call(cp_service.closeRatesTile, base_details.build())
    #
    #     except Exception:
    #         logging.error("Error execution", exc_info=True)
