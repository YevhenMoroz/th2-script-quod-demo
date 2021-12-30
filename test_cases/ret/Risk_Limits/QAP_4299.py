import logging
import os

from custom import basic_custom_actions as bca
from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from test_framework.old_wrappers.ret_wrappers import close_order_book, decorator_try_except
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, ExtractOrderTicketErrorsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from test_framework.old_wrappers import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def extract_error_message_order_ticket(base_request, order_ticket_service):
    # extract rates tile table values
    extract_errors_request = ExtractOrderTicketErrorsRequest(base_request)
    extract_errors_request.extract_error_message()
    result = call(order_ticket_service.extractOrderTicketErrors, extract_errors_request.build())
    return result


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_4299"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "5,000,000"
    client = "HAKKIM"
    lookup = "T55FD"
    order_type = "Limit"
    tif = "Day"
    price = "4.0"
    expected_value = "Error - [QUOD-11814] 'OrdQty' (1.1e+07) greater than 'MaxOrdQty' (1e+07)"
    # endregion

    # region Open FE
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create order according with step 1 and step 2
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, False, None, price, False, False, None)
    # end region

    # region Check values in OrderBook(expected result in step 2)
    eq_wrappers.verify_value(base_request, case_id, "Sts", "Open", False)
    eq_wrappers.verify_value(base_request, case_id, "Qty", qty, False)
    eq_wrappers.verify_value(base_request, case_id, "Limit Price", "4", False)
    # end region check value

    # region Amend order according with step 3
    order_amend = OrderTicketDetails()
    order_amend.set_quantity("11,000,000")
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request)
    amend_order_details.set_order_details(order_amend)

    call(order_book_service.amendOrder, amend_order_details.build())
    # end region

    # region Extract error in order ticket
    result_amend_qty = extract_error_message_order_ticket(base_request, order_ticket_service)
    close_order_book(base_request, Stubs.win_act_order_book)
    # end region extract

    # region verify details(expected result in step 3)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check error message in order ticket")
    verifier.compare_values("Amend error message", expected_value, result_amend_qty["ErrorMessage"])
    verifier.verify()
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")