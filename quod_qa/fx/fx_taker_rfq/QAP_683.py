import logging
import time
import rule_management as rm
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction, ExtractRFQTileValues, TableActionsRequest, TableAction, CellExtractionDetails
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile_swap(base_request, service, near_qty, cur1, cur2, near_tenor, far_tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_far_leg_tenor(far_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_value_in_column(exec_id, base_request, service, case_id):
    table_actions_request = TableActionsRequest(details=base_request)
    table_actions_request.set_extraction_id(exec_id)
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_best_bid_small("ar_rfq.extract_best_bid_small")
    extract1 = TableAction.extract_cell_value(CellExtractionDetails("PtsSell", "Pts", "HSB", 0))
    extract2 = TableAction.extract_cell_value(CellExtractionDetails("DistSell", "Dist", "HSB", 0))
    extract3 = TableAction.extract_cell_value(CellExtractionDetails("2WSell", "2W", "HSB", 0))
    extract4 = TableAction.extract_cell_value(CellExtractionDetails("SPSell", "SP", "HSB", 0))

    table_actions_request.add_actions([extract1, extract2, extract3, extract4])
    extract_data = call(service.extractRFQTileValues, extract_value.build())
    response = call(service.processTableActions, table_actions_request.build())
    extracted_best_bid = float(extract_data["ar_rfq.extract_best_bid_small"])
    extracted_pts = float(response["PtsSell"])
    extracted_dist = float(response["DistSell"])
    extracted_2w = float(response["2WSell"])
    extracted_sp = float(response["SPSell"])
    pts = round((extracted_2w - extracted_sp) * 10000, 1)
    dist = round(abs(extracted_best_bid - extracted_pts), 1)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check calculation Of Columns")
    verifier.compare_values("Dist", str(dist), str(extracted_dist))
    verifier.compare_values("Pts", str(pts), str(extracted_pts))
    verifier.verify()


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    # Rules
    rule_manager = rm.RuleManager()
    RFQ = rule_manager.add_RFQ('fix-fh-fx-rfq')
    TRFQ = rule_manager.add_TRFQ('fix-fh-fx-rfq')
    case_name = "QAP-683"
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_far_tenor = "2W"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "MMCLIENT2"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile_swap(base_rfq_details, ar_service, case_qty, case_from_currency,
                             case_to_currency, case_near_tenor, case_far_tenor, case_client)
        send_rfq(base_rfq_details, ar_service)
        cancel_rfq(base_rfq_details, ar_service)
        # Step 2-3
        check_value_in_column("CH_0", base_rfq_details, ar_service, case_id)



    except Exception as e:
        logging.error("Error execution", exc_info=True)

    finally:
        for rule in [RFQ, TRFQ]:
            rule_manager.remove_rule(rule)
