import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues, SelectRowsRequest, \
    DeselectRowsRequest, ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
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


def check_px(base_request, service, row):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidPx", "Px"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askPx", "Px"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    bid_px = response["rateTile.bidPx"]
    ask_px = response["rateTile.askPx"]
    return [bid_px, ask_px]


def check_base(base_request, service, row):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBase", "Base"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBase", "Base"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    bid_base = response["rateTile.bidBase"]
    ask_base = response["rateTile.askBase"]
    return [bid_base, ask_base]


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def press_pricing(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_pricing()
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


def compare_prices(case_id, ask_before, bid_before, ask_after, bid_after, pips, ):
    ask_difference = abs(round(ask_after - ask_before, 5))
    bid_difference = abs(round(bid_after - bid_before, 5))
    expected_dif = float(pips) / 10000
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices")
    verifier.compare_values("Price ask", str(expected_dif), str(ask_difference))
    verifier.compare_values("Price bid", str(expected_dif), str(bid_difference))
    verifier.verify()


def compare_margin_ask(case_id, ask_base_before, ask_base_after, pips, *args):
    difference = abs(round(ask_base_after - ask_base_before, 1))
    expected_difference = 0
    if "increase_ask" in args:
        expected_difference = float(pips)
    if "decrease_ask" in args:
        expected_difference = float(pips)
    if "narrow_spread" in args:
        expected_difference = float(pips)
    if "widen_spread" in args:
        expected_difference = float(pips)
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare spreads")
    verifier.compare_values("Spread", str(expected_difference), str(difference))
    verifier.verify()


def compare_margin_bid(case_id, bid_base_before, bid_base_after, pips, *args):
    difference = abs(round(bid_base_after - bid_base_before, 1))
    expected_difference = 0
    if "increase_bid" in args:
        expected_difference = float(pips)
    if "decrease_bid" in args:
        expected_difference = float(pips)
    if "narrow_spread" in args:
        expected_difference = float(pips)
    if "widen_spread" in args:
        expected_difference = float(pips)
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
    default_base = "0.2"

    try:
        # Step 1-2
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier, pips)
        # Step 3
        select_line(base_details, cp_service, [2])
        # Step 4
        base_before = check_base(base_details, cp_service, 2)
        px_before = check_px(base_details, cp_service, 2)
        modify_spread(base_details, cp_service, "narrow_spread")
        base_after = check_base(base_details, cp_service, 2)
        px_after = check_px(base_details, cp_service, 2)
        compare_margin_bid(case_id, base_before[0], base_after[0], pips, "narrow_spread")
        compare_margin_ask(case_id, base_before[1], base_after[1], pips, "narrow_spread")

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
