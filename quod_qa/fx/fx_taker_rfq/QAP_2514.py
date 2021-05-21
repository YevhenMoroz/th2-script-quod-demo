import logging
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def modify_rfq_tile(base_request, service, cur1, cur2, near_tenor, far_tenor, client):
    modify_request = ModifyRFQTileRequest(details=base_request)

    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_far_leg_tenor(far_tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_qty(exec_id, base_request, service, case_id, near_qty, far_qty):
    extract_value = ExtractRFQTileValues(details=base_request)
    extract_value.set_extraction_id(exec_id)
    extract_value.extract_quantity("aggrRfqTile.nearqty")
    extract_value.extract_far_leg_qty("aggrRfqTile.farqty")
    response = call(service.extractRFQTileValues, extract_value.build())
    extract_near_qty = response["aggrRfqTile.nearqty"].replace(',', '')
    extract_far_qty = response["aggrRfqTile.farqty"].replace(',', '')

    verifier = Verifier(case_id)
    verifier.set_event_name("Verify Qty in RFQ tile")
    verifier.compare_values('Near leg qty', str(near_qty), extract_near_qty[:-3])
    verifier.compare_values('Near far qty', str(far_qty), extract_far_qty[:-3])
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_client = "MMCLIENT2"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_tenor = "Spot"
    case_far_tenor = "1W"
    case_qty1 = 2000000
    case_qty2 = 3000000
    case_qty3 = 4000000
    case_qty4 = 1000000

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)
    modify_request = ModifyRFQTileRequest(details=base_rfq_details)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)
    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_from_currency, case_to_currency,
                        case_near_tenor, case_far_tenor, case_client)

        # Step 2
        modify_request.set_quantity(case_qty1)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty("RFQ", base_rfq_details, ar_service, case_id, case_qty1, case_qty1)

        # Step 3
        modify_request.set_far_leg_qty(case_qty2)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty("RFQ", base_rfq_details, ar_service, case_id, case_qty1, case_qty2)

        # Step 4
        modify_request.set_quantity(case_qty3)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty("RFQ", base_rfq_details, ar_service, case_id, case_qty3, case_qty2)

        # Step 5
        send_rfq(base_rfq_details, ar_service)
        cancel_rfq(base_rfq_details, ar_service)

        modify_request.set_quantity(case_qty4)
        call(ar_service.modifyRFQTile, modify_request.build())
        check_qty("RFQ", base_rfq_details, ar_service, case_id, case_qty4, case_qty4)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
