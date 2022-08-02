import logging
import os

from custom import basic_custom_actions as bca
from datetime import datetime
from custom.verifier import Verifier
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_ticket import ExtractOrderTicketValuesRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.ret_wrappers import close_order_book, try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def verifier_field_state(case_id, expected_value, field_state_response):
    # region verifier
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking disabled fields")
    verifier.compare_values("Disabled field", expected_value, field_state_response)
    verifier.verify()
    # end region


def extract_main_panel_order_ticket_fields_state(base_request, order_ticket_service):
    # extract rates tile table values
    extract_disclose_flag_request = ExtractOrderTicketValuesRequest(base_request)
    extract_disclose_flag_request.get_instrument_state()
    extract_disclose_flag_request.get_client_state()
    extract_disclose_flag_request.get_edit_venue_state()
    result = call(order_ticket_service.extractOrderTicketValues, extract_disclose_flag_request.build())
    print(result)
    return result


@try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_T3722"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    qty = "1000"
    price = "30"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create order via FE according with step 1
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, False, price, False, False,
                             None)
    # end region

    # region extract disabled field in order when we try to amend according with step 3,4
    field_state_response = extract_main_panel_order_ticket_fields_state(base_request, order_ticket_service)
    # end region

    # region verify response
    verifier_field_state(case_id, "False", field_state_response["INSTRUMENT"])
    verifier_field_state(case_id, "False", field_state_response["EDIT_VENUE"])
    verifier_field_state(case_id, "False", field_state_response["CLIENT"])
    # end region

    close_order_book(base_request, Stubs.win_act_order_book)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
