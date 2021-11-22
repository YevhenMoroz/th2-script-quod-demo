import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3293"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    price = "40"
    newPrice = "1"
    lookup = "PROL"
    client = "CLIENT_FIX_CARE"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # endregion
    param_list = {'Price': newPrice}
    response = fix_message.pop('response')
    # region check FIX CO
    params = {
        'Account': client,
        'OrderQty': qty,
        'ExecType': 'A',
        'OrdStatus': 'A',
        'Side': 1,
        'Price': price,
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
        'ExpireDate': '*',
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion

    # region check_out order
    eq_wrappers.check_out_order(base_request)
    # endregion
    # region check_out order
    eq_wrappers.verify_order_value(base_request, case_id, 'IsLocked', 'Yes', False)
    # endregion
    # region CancelOrderReplaceRequest sent
    fix_message = FixMessage(fix_message)
    test_framework.old_wrappers.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, param_list, client + "_PARIS")
    # endregion
    # check tag 58
    params = {
        'Account': client,
        'OrdStatus': '0',
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'OrderID': '*',
        'TransactTime': '*',
        'Text': '11629 Order is in locked state',
        'OrigClOrdID': '*'
    }
    fix_verifier_ss.CheckCancelReject(params, response, message_name='Check params',
                                      key_parameters=['ClOrdID', 'OrdStatus'])
    # endregion

    # check in Order
    eq_wrappers.check_in_order(base_request)
    # endregion
    time.sleep(1)
    # region resend ORDER_CANCEL_REPLACE_REQUEST
    test_framework.old_wrappers.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, param_list, client + "_PARIS")
    # endregion

    # region  accept modify
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion

    # region check isLocked
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("IsLocked from View", eq_wrappers.get_order_value(base_request, "IsLocked"), ''),
    verifier.verify()
    # endregion

    # region verify fix message

    params = {
        'OrderQty': qty,
        'ExecType': 5,
        'OrdStatus': 0,
        'Side': 1,
        'Price': newPrice,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
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
        'OrigClOrdID': '*'
    }
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion
