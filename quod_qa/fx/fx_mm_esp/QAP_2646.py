import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def increase_margin(base_request, service, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_pips(pips)
    modify_request.widen_spread()
    call(service.modifyRatesTile, modify_request.build())


def decrease_margin(base_request, service, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_pips(pips)
    modify_request.narrow_spread()
    call(service.modifyRatesTile, modify_request.build())


def restore_default_margins(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def check_ask_price(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask = response["rates_tile.ask_pips"]
    return ask


def compare_prices(case_id, ask_before, ask_after):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices after change margins")
    verifier.compare_values("Prices", ask_before, ask_after, VerificationMethod.NOT_EQUALS)
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    securityType = 'FXSPOT',
    instrument_gbp_nok = "GBP/NOK-SPOT"
    def_md_symbol_gbp_usd = "GBP/USD:SPO:REG:HSBC"
    symbol_gbp_usd = 'GBP/USD'
    instrument_gbp_usd = "GBP/USD-SPOT"
    instrument_usd_nok = "USD/NOK-SPOT"
    def_md_symbol_usd_nok = "USD/NOK:SPO:REG:HSBC"
    symbol_usd_nok = 'USD/NOK'
    client_tier = "Silver"

    case_base_request = get_base_request(session_id, case_id)
    base_details_nok_sek = BaseTileDetails(base=case_base_request, window_index=0)
    base_details_usd_sek = BaseTileDetails(base=case_base_request, window_index=1)
    base_details_usd_nok = BaseTileDetails(base=case_base_request, window_index=2)

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_details_nok_sek, cp_service)
        create_or_get_rates_tile(base_details_usd_sek, cp_service)
        create_or_get_rates_tile(base_details_usd_nok, cp_service)

        modify_rates_tile(base_details_nok_sek, cp_service, instrument_gbp_nok, client_tier)
        modify_rates_tile(base_details_usd_sek, cp_service, instrument_gbp_usd, client_tier)
        modify_rates_tile(base_details_usd_nok, cp_service, instrument_usd_nok, client_tier)

        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_gbp_usd, symbol_gbp_usd)).send_market_data_spot()
        FixClientBuy(CaseParamsBuy(case_id, def_md_symbol_usd_nok, symbol_usd_nok)).send_market_data_spot()

        # Step 2
        price_before_increase = check_ask_price(base_details_nok_sek, cp_service)
        increase_margin(base_details_usd_sek, cp_service, "500")
        price_after_increase = check_ask_price(base_details_nok_sek, cp_service)
        compare_prices(case_id, price_before_increase, price_after_increase)
        # Step 3
        decrease_margin(base_details_usd_sek, cp_service, "")
        price_after_decrease = check_ask_price(base_details_nok_sek, cp_service)
        compare_prices(case_id, price_after_increase, price_after_decrease)
        # Step 4
        price_before_increase = check_ask_price(base_details_nok_sek, cp_service)
        increase_margin(base_details_usd_nok, cp_service, "500")
        price_after_increase = check_ask_price(base_details_nok_sek, cp_service)
        compare_prices(case_id, price_before_increase, price_after_increase)
        decrease_margin(base_details_usd_nok, cp_service, "")
        price_after_decrease = check_ask_price(base_details_nok_sek, cp_service)
        compare_prices(case_id, price_after_increase, price_after_decrease)

        # Use Defaults
        restore_default_margins(base_details_usd_sek, cp_service)
        restore_default_margins(base_details_usd_nok, cp_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details_nok_sek.build())
            call(cp_service.closeRatesTile, base_details_usd_sek.build())
            call(cp_service.closeRatesTile, base_details_usd_nok.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
