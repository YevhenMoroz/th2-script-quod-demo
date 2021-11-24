import logging
import time
from datetime import datetime, date, timedelta

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    global fix_message, nos_rule
    case_name = "QAP-2008"
    rule_manager = RuleManager()
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "800"
    qty2 = "1500"
    client = "CLIENT1"
    price = 3
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion

    # region Create order via FIX

    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(), 'XPAR_' + client, "XPAR", price)

        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 2, client, 2, qty, 6, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    response = fix_message.pop('response')
    # region Check
    params = {
        'OrderQty': qty,
        'ExecType': 'A',
        'OrdStatus': 'A',
        'Side': '2',
        'Account':'*',
        'Price': price,
        'TimeInForce': '6',
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
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        ''
        'header': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'], direction='SECOND')
    # endregion
    # endregion

    # region Amend order
    try:
        nos_rule = rule_manager.add_OrderCancelReplaceRequest(test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(), 'XPAR_' + client,
                                                              'XPAR', True)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, {'OrderQty': qty2})
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion

    # region Check values after Amending
    params = {
        'OrderQty': qty2,
        'ExecType': '5',
        'Account': '*',
        'OrdStatus': '0',
        'TradeDate': '*',
        'Side': '2',
        'Price': price,
        'TimeInForce': '6',
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
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'LastCapacity': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ExecType'],direction='SECOND')
    # endregion

    # region Cancelling order
    try:
        nos_rule = rule_manager.add_OrderCancelRequest(test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(), 'XPAR_' + client, 'XPAR',
                                                       True)
        cl_ord_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
        test_framework.old_wrappers.eq_fix_wrappers.cancel_order_via_fix(cl_ord_id, cl_ord_id, client, case_id, 2)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion

    # region Check values after Cancel
    params = {
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': '2',
        'Price': price,
        'TimeInForce': '6',
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
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ExecType'])
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
