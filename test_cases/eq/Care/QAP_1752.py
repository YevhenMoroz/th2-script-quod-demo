import logging

from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum, ExtractOrderTicketValuesRequest

from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers, eq_fix_wrappers
from test_cases.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1723"
    # region Declarations
    qty = "900"
    price = "50"
    client = "CLIENT_FIX_CARE"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion
    # region Create CO order
    fix_message=eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    response = fix_message.pop("response")
    # endregion
    # region Cancel
    cl_ord_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
    eq_fix_wrappers.cancel_order_via_fix(case_id,cl_ord_id,cl_ord_id,client,1)
    # endregion
    # region Check values after Cancel
    params = {
        'Account': client,
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': '1',
        'Price': price,
        'TimeInForce': '0',
        'ClOrdID': cl_ord_id,
        'OrigClOrdID': cl_ord_id,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'CxlQty': '*',
        'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss = FixVerifier(eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params')
    # endregion
