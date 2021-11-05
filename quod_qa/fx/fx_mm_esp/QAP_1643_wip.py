import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues, SelectRowsRequest, \
    DeselectRowsRequest
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


def select_line(base_request, service, line):
    modify_request = SelectRowsRequest(details=base_request)
    modify_request.set_row_numbers(line)
    call(service.selectRows, modify_request.build())


def deselect_line(base_request, service):
    modify_request = DeselectRowsRequest(details=base_request)
    call(service.deselectRows, modify_request.build())


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def modify_spread(base_request, service, *args):
    modify_request = ModifyRatesTileRequest(details=base_request)
    if "increase_ask" in args:
        modify_request.increase_ask()
    if "decrease_ask" in args:
        modify_request.decrease_ask()
    if "increase_bid" in args:
        modify_request.increase_bid()
    if "decrease_bid" in args:
        modify_request.decrease_bid()
    if "narrow_spread" in args:
        modify_request.narrow_spread()
    if "widen_spread" in args:
        modify_request.widen_spread()
    if "skew_towards_ask" in args:
        modify_request.skew_towards_ask()
    if "skew_towards_bid" in args:
        modify_request.skew_towards_bid()
    call(service.modifyRatesTile, modify_request.build())


def check_bid(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_bid_large_value("rates_tile.bid_large")
    extract_value_request.extract_bid_pips("rates_tile.bid_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    bid = float(response["rates_tile.bid_large"] + response["rates_tile.bid_pips"])
    return float(bid)


def check_ask(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask = float(response["rates_tile.ask_large"] + response["rates_tile.ask_pips"])
    return float(ask)


def compare_prices(case_id, ask_before, bid_before, ask_after, bid_after, pips, ):
    ask_difference = abs(round(ask_after - ask_before, 5))
    bid_difference = abs(round(bid_after - bid_before, 5))
    expected_dif = float(pips) / 10000
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices")
    verifier.compare_values("Price ask", str(expected_dif), str(ask_difference))
    verifier.compare_values("Price bid", str(expected_dif), str(bid_difference))
    verifier.verify()


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
    return float(extracted_spread)


def compare_spreads(case_id, spread_before, spread_after, pips, *args):
    difference = abs(round(spread_after - spread_before, 1))
    expected_difference = 0
    if "increase_ask" in args:
        expected_difference = float(pips)
    if "decrease_ask" in args:
        expected_difference = float(pips)
    if "increase_bid" in args:
        expected_difference = float(pips)
    if "decrease_bid" in args:
        expected_difference = float(pips)
    if "narrow_spread" in args:
        expected_difference = float(pips) * 2
    if "widen_spread" in args:
        expected_difference = float(pips) * 2
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare spreads")
    verifier.compare_values("Spread", str(expected_difference), str(difference))
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
    default_base="0.2"

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier, pips)
        select_line(base_details, cp_service, [2])
        # Step 2
        spread_before = check_spread(base_details, cp_service, case_id)
        # Step 3
        modify_spread(base_details, cp_service, "narrow_spread")
        spread_after = check_spread(base_details, cp_service, case_id)
        compare_spreads(case_id, spread_before, spread_after, pips, "narrow_spread")
        # Step 4
        spread_before = check_spread(base_details, cp_service, case_id)
        modify_spread(base_details, cp_service, "widen_spread")
        spread_after = check_spread(base_details, cp_service, case_id)
        compare_spreads(case_id, spread_before, spread_after, pips, "widen_spread")
        # Step 5
        spread_before = check_spread(base_details, cp_service, case_id)
        modify_spread(base_details, cp_service, "increase_ask")
        spread_after = check_spread(base_details, cp_service, case_id)
        compare_spreads(case_id, spread_before, spread_after, pips, "increase_ask")
        # Step 6
        spread_before = check_spread(base_details, cp_service, case_id)
        modify_spread(base_details, cp_service, "decrease_bid")
        spread_after = check_spread(base_details, cp_service, case_id)
        compare_spreads(case_id, spread_before, spread_after, pips, "decrease_bid")
        # Step 7
        ask_before = check_ask(base_details, cp_service)
        bid_before = check_bid(base_details, cp_service)
        modify_spread(base_details, cp_service, "skew_towards_ask")
        ask_after = check_ask(base_details, cp_service)
        bid_after = check_bid(base_details, cp_service)
        compare_prices(case_id, ask_before, bid_before, ask_after, bid_after, pips)
        # Step 8
        ask_before = check_ask(base_details, cp_service)
        bid_before = check_bid(base_details, cp_service)
        modify_spread(base_details, cp_service, "skew_towards_bid")
        ask_after = check_ask(base_details, cp_service)
        bid_after = check_bid(base_details, cp_service)
        compare_prices(case_id, ask_before, bid_before, ask_after, bid_after, pips)

        deselect_line(base_details, cp_service)
        use_default(base_details, cp_service)


    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
