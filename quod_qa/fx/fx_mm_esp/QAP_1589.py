import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from win_gui_modules.order_book_wrappers import ExtractionDetail


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    modify_request.set_pips(pips)
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


def live_toggle(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.toggle_live()
    call(service.modifyRatesTile, modify_request.build())


def use_defaults_click(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def extract_column_base(base_request, service):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, DeselectRowsRequest
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(1)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("bid", "Base"))
    extract_table_request.set_ask_extraction_field(ExtractionDetail("ask", "Base"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    deselect_rows_request = DeselectRowsRequest(details=base_request)
    call(service.deselectRows, deselect_rows_request.build())
    return response


def check_margins(case_id, initial_margin, changed_margin, live_margin, live_off_margin, use_default_margin):
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking margins bid")
    verifier.compare_values(f'After live toggle off', initial_margin.get('bid'), live_off_margin.get('bid'))
    verifier.compare_values(f'After live toggle on', changed_margin.get('bid'), live_margin.get('bid'))
    verifier.compare_values(f'After use defaults', initial_margin.get('bid'), use_default_margin.get('bid'))
    verifier.verify()

    verifier.set_event_name("Checking margins ask")
    verifier.compare_values(f'After live toggle off', initial_margin.get('ask'), live_off_margin.get('ask'))
    verifier.compare_values(f'After live toggle on', changed_margin.get('ask'), live_margin.get('ask'))
    verifier.compare_values(f'After use defaults', initial_margin.get('ask'), use_default_margin.get('ask'))
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
    pips = "50"

    try:

        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)

        # Step 1

        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier, pips)

        # Step 2

        initial_margin = extract_column_base(base_details, cp_service)
        modify_spread(base_details, cp_service, "widen_spread")
        modified_margin = extract_column_base(base_details, cp_service)

        # Step 3

        live_toggle(base_details, cp_service)
        live_toggle_off_margin = extract_column_base(base_details, cp_service)

        # Step 4

        live_toggle(base_details, cp_service)
        live_toggle_on_margin = extract_column_base(base_details, cp_service)

        # Step 5

        use_defaults_click(base_details, cp_service)
        use_default_margin = extract_column_base(base_details, cp_service)

        # Step 6

        check_margins(
            case_id, initial_margin, modified_margin,
            live_toggle_on_margin, live_toggle_off_margin, use_default_margin
        )

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
