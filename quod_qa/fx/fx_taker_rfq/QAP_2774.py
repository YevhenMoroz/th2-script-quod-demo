import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ExtractRFQTileValues
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def check_client_and_beneficiary(base_request, service, case_id, client, beneficiary):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_beneficiary("aggrRfqTile.beneficiary")
    extract_value.extract_client("aggrRfqTile.client")
    response = call(service.extractRFQTileValues, extract_value.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check client and Beneficiary")
    verifier.compare_values("Client", client, response["aggrRfqTile.client"])
    verifier.compare_values("Beneficiary", beneficiary, response["aggrRfqTile.beneficiary"])
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    # Default client and beneficiary on quod309
    client = "FIRM_1"
    beneficiary = "[Beneficiary]"

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

        # Step 2
        check_client_and_beneficiary(base_rfq_details, ar_service, case_id,
                                     client, beneficiary)
        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
