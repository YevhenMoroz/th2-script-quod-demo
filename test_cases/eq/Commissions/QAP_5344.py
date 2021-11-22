import logging
import time

import test_cases.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_cases.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5344"
    qty = "5000"
    client = "MOClient"
    price = 5
    side = 2
    tif = 1
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity()
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingle_Market(buy_connectivity, client + "_PARIS", "XPAR", True, int(qty),
                                                        price)
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 1, side, client, 1, qty, tif)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    params = {
        'OrderQtyData': '*',
        'ExecType': 'F',
        'OrdStatus': '2',
        'Side': side,
        'TimeInForce': tif,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': response.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'Account': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'Instrument': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'SettlDate': '*',
        'LastExecutionPolicy': '*',
        'TradeDate': '*',
        'SecondaryOrderID': '*',
        'LastMkt': '*',
        'Text': '*',
        'SettlType': '*',
        'ExecBroker': '*',
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'NoMiscFees': [
            {
                'MiscFeeAmt': '*',
                'MiscFeeCurr': '*',
                'MiscFeeType': '*'
            }
        ],
        'GrossTradeAmt': '*',
        'CommissionData': '*'
    }
    fix_verifier_ss = FixVerifier(test_cases.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params')
