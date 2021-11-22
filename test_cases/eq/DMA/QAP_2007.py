import logging
import time

import test_cases.wrapper.eq_fix_wrappers
from test_cases.wrapper.fix_verifier import FixVerifier

from custom.basic_custom_actions import create_event, timestamps

from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    global fix_message, nos_rule, rule_manager
    case_name = "QAP-2007"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    client = 'CLIENT4'
    price = "40"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion

    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingle_FOK(test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(), client + '_PARIS', 'XPAR',
                                                     False, float(price))
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 4, price)
    finally:
        time.sleep(10)
        rule_manager.remove_rule(nos_rule)
        response = fix_message.pop('response')

    # region Check values in OrderBook
    params = {
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': 1,
        'Text': '*',
        'TimeInForce': 4,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'ExpireDate': '*',
        'SettlDate': '*',
        'Currency': '*',
        'Price': 40,
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'SettlType': '*',
        'OrdType': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
        'CxlQty': qty
    }

    fix_verifier_ss = FixVerifier(test_cases.wrapper.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'OrdStatus'])
    # endregion
    # endregion

    # logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
