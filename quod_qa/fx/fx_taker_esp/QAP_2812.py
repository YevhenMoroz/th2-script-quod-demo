import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ContextActionRatesTile, ModifyRatesTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_esp_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_esp_tile(base_request, service, from_c, to_c, tenor):
    from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_currency=from_c, to_currency=to_c, set_tenor=tenor)
    call(service.modifyRatesTile, modify_request.build())


def check_price_esp(base_request, service, case_id):
    from win_gui_modules.aggregated_rates_wrappers import ExtractRatesTileDataRequest
    extraction_value = ExtractRatesTileDataRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_value.set_extraction_id(extraction_id)
    extraction_value.extract_best_bid("ratesTile.Bid")
    extraction_value.extract_best_ask("ratesTile.Ask")
    response = call(service.extractRatesTileValues, extraction_value.build())
    bid = response["ratesTile.Bid"]
    ask = response["ratesTile.Ask"]
    verifier = Verifier(case_id)
    verifier.set_event_name("Check prices on ESP tile")
    verifier.compare_values("Bid price", 'Not null', bid, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Ask price", 'Not null', ask, VerificationMethod.NOT_EQUALS)
    verifier.verify()


def add_full_amount(base_tile_details, service):
    modify_request = ModifyRatesTileRequest(details=base_tile_details)
    action0 = ContextActionRatesTile().add_full_amount_qty("1")
    action = ContextActionRatesTile().add_full_amount_qty("3")
    action2 = ContextActionRatesTile().open_full_amount()
    modify_request.add_context_actions([action2, action, action0])
    call(service.modifyRatesTile, modify_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    try:
        # Step 1
        create_or_get_esp_tile(base_details, ar_service)
        add_full_amount(base_details, ar_service)
        modify_esp_tile(base_details, ar_service, from_curr, to_curr, tenor)
        # Step 2
        check_price_esp(base_details, ar_service, case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tiles
            call(ar_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
