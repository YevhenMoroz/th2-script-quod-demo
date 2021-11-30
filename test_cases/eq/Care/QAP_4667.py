import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4667"
    # region Declarations
    qty = "800"
    client = "CLIENT_FIX_CARE"
    price = "40"
    price2 = '200'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    # endregion
    # region Create order via FIX
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 4, qty, 1, price, stop_price=price)
    response = fix_message.pop('response')
    # endregion
    # region Check values in OrderBook
    eq_wrappers.accept_order('VETO', qty, price)
    test_framework.old_wrappers.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, {'StopPx': price2, 'TimeInForce': 0})
    eq_wrappers.reject_order('VETO', qty, price)
    eq_wrappers.verify_order_value(base_request, case_id, 'Stop Price', price, False)
    eq_wrappers.verify_order_value(base_request, case_id, 'TIF', 'GoodTillCancel', False)
    params = {
        'OrderQty': qty,
        'ExecType': '0',
        'Account': '*',
        'OrdStatus': '0',
        'Side': 2,
        'TimeInForce': 1,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'Price': price,
        'StopPx': price,
        'SettlDate': '*',
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
        'SettlType': '*'
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'StopPx', 'ExecType'])
    # endregion
