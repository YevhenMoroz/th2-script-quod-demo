import logging
import time
from copy import deepcopy
from datetime import date, timedelta
import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from test_cases.wrapper import eq_wrappers, eq_fix_wrappers
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# need to modify
def execute(report_id, session_id):
    case_name = "QAP-2005"
    timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    price = 20
    price2 = 19
    client = 'CLIENT1'
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion
    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            eq_fix_wrappers.get_buy_connectivity(),
            "XPAR_" + client, 'XPAR', price)
        fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 1, 2, client, 2, qty, 0, price)
    except:
        rule_manager.remove_rule(nos_rule)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    response = fix_message.pop('response')
    fix_message = FixMessage(fix_message)
    eq_fix_wrappers.amend_order_via_fix(case_id,fix_message,{'Price': price2})

    fix_manager = FixManager(eq_fix_wrappers.sell_connectivity, case_id)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OrderCancelReplaceRequest(eq_fix_wrappers.get_buy_connectivity(), "XPAR_" + client,
                                                          "XPAR", True)
        fix_modify_message = deepcopy(fix_message)
        fix_modify_message.change_parameters({'Price': price2})
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(rule)
    # endregion
    cl_order_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
    params = {
        'ExecType': '5',
        'OrdStatus': '0',
        'Side': '2',
        'TimeInForce': '0',
        'ClOrdID': cl_order_id,
        'OrigClOrdID': cl_order_id,
        'OrderQtyData': {'OrderQty': qty},
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'ExecBroker': '*',
        'Price': price2,
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'TransactTime': '*',
        'Text': 'order replaced',
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
        'SettlType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
    }
    fix_verifier_bo = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckExecutionReport(params, response, ['ClOrdID', 'ExecType'])
    # region Cancelling order

