import logging
import time
import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-2000"
    # region Declarations
    qty = "900"
    client = "CLIENT1"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    # endregion
    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingle_Market_FIXStandard(buy_connectivity, "XPAR_" + client, "XPAR", True, 0, 0)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 2, client, 1, qty, 0)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # region Check values in OrderBook
    params = {
        'Account': client,
        'OrderQtyData': {'OrderQty': qty},
        #'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': 2,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'ExpireDate': '*',
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
        'Parties': '*',
        'Instrument': '*',
        'CxlQty': qty,
        'SettlType': '0'
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response,['ClOrdID','OrdStatus'])
    # endregion
