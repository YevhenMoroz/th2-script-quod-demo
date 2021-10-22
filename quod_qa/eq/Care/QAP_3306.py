import logging

import quod_qa.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def get_params(response, qty, order_sts, side, account):
    params = {
        'Account': account,
        'OrderQty': qty,
        'ExecType': 'F',
        'ExpireDate': '*',
        'OrdStatus': order_sts,
        'TradeDate': '*',
        'Side': side,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastCapacity': '*',
        'LastMkt': '*',
        'ChildOrderID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'VenueType': '*'
    }
    return params


def execute(report_id, session_id):
    case_name = "QAP-3306"

    # region Declarations
    qty3 = "100"
    qty2 = "70"
    qty1 = "30"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregionA
    # region Create CO
    fix_message1 = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 1, int(qty1), 0)
    eq_wrappers.accept_order(lookup, qty1, "0")
    fix_message2 = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 1, int(qty2), 0)
    eq_wrappers.accept_order(lookup, qty2, "0")
    fix_message3 = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 1, int(qty3), 0)
    eq_wrappers.accept_order(lookup, qty3, "0")
    response1 = fix_message1.pop('response')
    response2 = fix_message2.pop('response')
    response3 = fix_message3.pop('response')
    # endregion
    # region Manual Cross
    eq_wrappers.manual_cross_orders(base_request, qty2, price, [1, 2], "BSML")
    # endregion
    # region Verify
    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(get_params(response2, qty2, "2", 2, client), response1,
                                         None)
    # endregion
    # region Manual Cross
    eq_wrappers.manual_cross_orders(base_request, qty3, price, [1, 3], "BSML")
    # endregion
    # region Verify
    fix_verifier_ss.CheckExecutionReport(get_params(response1, qty1, "2", 2, client), response1,
                                         None)
    # endregion
