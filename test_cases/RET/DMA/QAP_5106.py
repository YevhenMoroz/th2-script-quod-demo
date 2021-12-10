import logging
import os

from datetime import datetime

from custom.basic_custom_actions import timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from test_framework.old_wrappers.ret_wrappers import create_order_extracting_error, extract_error_message_order_ticket, verifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = "QAP-4169"

    seconds, nanos = timestamps()  # Store case start time

    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Declarations

    qty = "1300"
    price = "20"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "TCS"
    side = 'Sell'
    pos_validity = "Intraday"
    expected_value = "Error - [QUOD-24812] Invalid 'PosValidity'"
    # end region

    # region Create order step 2
    create_order_extracting_error(base_request, qty, client, lookup, tif, side, order_type, price, pos_validity)
    # end region

    # region Extract and Verify error message from order ticket
    error_message = extract_error_message_order_ticket(base_request, Stubs.win_act_order_ticket)
    verifier(case_id, event_name="Check Error Message", expected_value=expected_value,
             actual_value=error_message["ErrorMessage"][0:42])
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")