import logging
from datetime import datetime

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from win_gui_modules.utils import set_session_id
from win_gui_modules.wrappers import set_base
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3886"
    # region Declarations
    current_datetime = datetime.now()
    qty = "800"
    client = "CLIENT2"
    price = '40'
    instrument = {
        'Symbol': 'IS0000000001_EUR',
        'SecurityID': 'IS0000000001',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XEUR'
    }
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    # endregion
    # region Create order via FIX
    if current_datetime.month < 10:
        curent_month = '0' + str(current_datetime.month)
    else:
        curent_month = str(current_datetime.month)
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
                                                                             'EUREX_' + client, 'XEUR', float(price))
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 6, price, insrument=instrument)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(10)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # region Check values in OrderBook
    params = {
        'OrderQty': qty,
        'ExecType': '0',
        'OrdStatus': '0',
        'Account': '*',
        'ReplyReceivedTime':'*',
        'Side': 1,
        'TimeInForce': 6,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'Price': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'ExpireDate': '*',
        'Text': '*',
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
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
        'SettlType': '0',
        'SettlDate': str(current_datetime.year) + curent_month + str(current_datetime.day + 4)
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
