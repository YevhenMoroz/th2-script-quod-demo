import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5611"
    qty = "5611"
    client = "MOClient"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()

    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingle_Market(buy_connectivity, client + "_PARIS", "XPAR", True, int(qty), 50)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 2, client, 1, qty, 1)
        response = fix_message.pop('response')
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    order_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
    cl_order_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
    test_framework.old_wrappers.eq_fix_wrappers.cancel_order_via_fix(case_id, order_id, cl_order_id, client, 2)

    params = {
        'Account': client,
        'OrdStatus': '2',
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'OrderID': '*',
        'TransactTime': '*',
        'Text': '11629 Order is already in terminate state',
        'OrigClOrdID': '*'
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckCancelReject(params, response, key_parameters=['ClOrdID', 'OrdStatus', ])
