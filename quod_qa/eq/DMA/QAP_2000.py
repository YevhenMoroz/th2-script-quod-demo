import logging
from datetime import datetime
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from win_gui_modules.utils import set_session_id
from win_gui_modules.wrappers import set_base
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2000"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    client = "CLIENTYMOROZ"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    # endregion
    # region Create order via FIX
    try:
        rule_manager = RuleManager()

        rule = rule_manager.add_NewOrdSingle_Market("fix-bs-310-columbia", client+"_PARIS", "XPAR", False, int(qty),
                                                    20.0)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 2, client, 1, qty, 0)
        response = fix_message.pop('response')
    finally:
        rule_manager.remove_rule(rule)
    # endregion
    # region Check values in OrderBook
    params = {
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': 2,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
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
        'SettlType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
    }
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])

    # endregion
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
