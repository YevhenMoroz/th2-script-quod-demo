import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, \
    ContextAction, ExtractRFQTileValues, TableActionsRequest, TableAction, CellExtractionDetails
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, tenor, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filter(venues)
    modify_request.add_context_action(action)
    modify_request.set_quantity(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_value_in_column(exec_id, base_request, service, case_id, venue):
    table_actions_request = TableActionsRequest(details=base_request)
    table_actions_request.set_extraction_id(exec_id)
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_best_bid_large("ar_rfq.extract_best_bid_large")
    extract1 = TableAction.extract_cell_value(CellExtractionDetails("PtsSell", "Pts", venue, 0))
    extract2 = TableAction.extract_cell_value(CellExtractionDetails("SP_Sell", "SP", venue, 0))
    extract3 = TableAction.extract_cell_value(CellExtractionDetails("1W_Sell", "1W", venue, 0))

    table_actions_request.add_actions([extract1, extract2, extract3])
    response = call(service.processTableActions, table_actions_request.build())
    best_bid = call(service.extractRFQTileValues, extract_value.build())

    extracted_large = best_bid["ar_rfq.extract_best_bid_large"]
    extracted_sp = response["SP_Sell"]
    price = float(best_bid["ar_rfq.extract_best_bid_large"] + response["PtsSell"])
    if len(extracted_sp) <= 3:
        column_sp = float(extracted_large + extracted_sp)
    else:
        column_sp = float(extracted_sp)

    extracted_1w = response["1W_Sell"]

    column_1w = round(price - column_sp, 5)

    def check_dif():
        if int((float(extracted_1w) * 0.0001 - column_1w) * 10000) <= 1:
            return str(extracted_1w)
        else:
            return str(column_1w)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check calculation 1W")
    verifier.compare_values("1W", check_dif(), str(extracted_1w))
    verifier.verify()


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_qty = 1000000
    case_near_tenor = "1W"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "ASPECT_CITI"
    venues = "CITI"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_near_tenor, case_client, venues)
        # Step 2
        send_rfq(base_rfq_details, ar_service)
        cancel_rfq(base_rfq_details, ar_service)
        check_value_in_column("ChWK1_0", base_rfq_details, ar_service, case_id, venues)
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
