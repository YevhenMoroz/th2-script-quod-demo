import logging

import quod_qa.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-2001"
    # region Declarations
    qty = "900"
    client = "CLIENT1"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion

    # region Create and execute order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_MarketNewOrdSingle_IOC(quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(), "XPAR_" + client, "XPAR",
                                                           True, 450, 5)
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 2, client, 1, qty, 3)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)

    # endregion

    # region Check values in OrderBook
    params = {
        'OrderQty': qty,
        'ExecType': 'F',
        'OrdStatus': '1',
        'Account': 'CLIENT1',
        'Side': 2,
        'Text': '*',
        'TimeInForce': 3,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'LastExecutionPolicy': '*',
        'TradeDate': '*',
        'AvgPx': '*',
        'ExpireDate': '*',
        'SettlDate': '*',
        'Currency': '*',
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
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }

    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'OrdStatus'])

    # endregion
