import os

import logging

from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps

from stubs import Stubs

from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from quod_qa.wrapper.eq_wrappers import create_order, get_order_id, verify_order_value
from custom.verifier import Verifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_book_service = Stubs.win_act_order_book

    lookup = "RELIANCE"
    order_type = "Limit"
    price = "15"
    qty = "20000001"
    tif = "Day"
    client = "HAKKIM"
    recipient = "RIN-DESK (CL)"
    free_notes = "11822 Calculated CumOrdQty"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # end region

    # region Create order via FE according to 1st step
    create_order(base_request, qty, client, lookup, order_type, tif,
                 True, recipient, price, None, None, False, DiscloseFlagEnum.DEFAULT_VALUE, None, False)
    # end region

    order_id = get_order_id(base_request)

    # region Check values in OrderBook according to 2nd step
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_details.set_filter(["Order ID", order_id])

    order_status = ExtractionDetail("order_status", "Sts")
    order_free_notes = ExtractionDetail("order_free_notes", "FreeNotes")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_free_notes
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    column_data = call(order_book_service.getOrdersDetails, order_details.request())
    actual_free_notes = column_data['order_free_notes']  # get the needed dictionary value

    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verify_order_value(base_request, case_id, "Sts", "Rejected", False)
    # using custom verifier to get slice of column content (verify_ent() get path as argument, not the string's content)
    verifier.compare_values("FreeNotes", free_notes, actual_free_notes[:26])
    verifier.verify()
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
