import os

import logging

from datetime import datetime

from custom import basic_custom_actions as bca

from custom.basic_custom_actions import timestamps
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails

from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from win_gui_modules.order_ticket_wrappers import NewOrderDetails

from quod_qa.wrapper.ret_wrappers import extract_parent_order_details, verifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def create_order(base_request, qty, client, order_type, price, tif, side, lookup, recipient, partial_desk,
                 disclose_flag):
    order_ticket_service = Stubs.win_act_order_ticket
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_limit(price)
    order_ticket.set_tif(tif)
    order_ticket.set_care_order(recipient, partial_desk, disclose_flag)
    if side == 'Buy':
        order_ticket.buy()
    else:
        order_ticket.sell()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())


def execute(session_id, report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    lookup = "RELIANCE"  # Setting values for all orders
    order_type = "Limit"
    price = "10"
    qty = "200"
    tif = "Day"
    client = "HAKKIM"
    side = "Buy"
    recipient = "RIN-DESK (CL)"
    partial_desk = False
    disclose_flag = DiscloseFlagEnum.DEFAULT_VALUE
    # endregion

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Create order via FE according to 1st step
    create_order(base_request, qty, client, order_type, price, tif, side, lookup, recipient, partial_desk,
                 disclose_flag)
    # endregion

    # region Check values in OrderBook according to 2nd step
    order_sts = extract_parent_order_details(base_request, column_name='Sts', extraction_id='Sts')
    verifier(case_id, event_name='Check order Status', expected_value='Held', actual_value=order_sts)

    order_gating_rule_name = extract_parent_order_details(base_request, column_name='GatingRuleName',
                                                          extraction_id='GatingRuleName')
    verifier(case_id, event_name='Check order GatingRuleName', expected_value='QAP-4282(Gr_for_Care)',
             actual_value=order_gating_rule_name)

    order_gating_rule_cond_name = extract_parent_order_details(base_request, column_name='GatingRuleCondName',
                                                               extraction_id='GatingRuleCondName')
    verifier(case_id, event_name='Check order GatingRuleCondName', expected_value='CareTinyQty',
             actual_value=order_gating_rule_cond_name)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
