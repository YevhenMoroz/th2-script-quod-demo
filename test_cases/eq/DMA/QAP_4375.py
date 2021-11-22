import logging
from datetime import datetime, date, timedelta

import test_cases.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from test_cases.wrapper import eq_wrappers
from test_cases.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# need to modify
def execute(report_id, session_id):
    case_name = "QAP-4375"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = 10000
    client = 'CLIENT4'
    expireDate = date.today() + timedelta(2)
    time = datetime.utcnow().isoformat()
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + "_PARIS", 'XPAR', float(price))
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price, no_allocs=
        [
            {
                'AllocAccount': 'CareWB',
                'AllocQty': qty
            }
        ]
                                                                              )
        response = fix_message.pop('response')
    finally:
        rule_manager.remove_rule(nos_rule)
    params = {
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': 2,
        'TimeInForce': 2,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
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
        'CxlQty': qty,
        'OrdType': '*',
        'Text': '11642 Unknown account identifier: CareWB / 11505 Runtime error (trying to get VSecurityAccount with an empty key)',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlType': '*',
        ''
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
    }
    fix_verifier_ss = FixVerifier(test_cases.wrapper.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
