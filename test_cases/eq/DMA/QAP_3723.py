import logging

import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
import time
from rule_management import RuleManager
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3723"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "800"
    price = "50"
    client = "CLIENT4"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregionA

    # region Create order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', float(price))
        nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', float(price),
            traded_qty=int(int(qty) / 2), delay=0)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
        eq_wrappers.complete_order(base_request)
        eq_wrappers.notify_dfd(base_request)
        response = fix_message.pop('response')
    finally:
        time.sleep(8)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule1)
    # endregion

    params = {
        'OrderQty': qty,
        'ExecType': '0',
        'Account': client,
        'OrdStatus': '0',
        # 'TradeDate': '*',
        'Side': 1,
        'Price': price,
        'TimeInForce': 1,
        'ClOrdID': eq_wrappers.get_cl_order_id(base_request),
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
        'ExpireDate': '*',
        'QtyType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params1',
                                         key_parameters=['ExecType', 'OrdStatus'], direction='FIRST')
    params1 = {
        'OrderQty': qty,
        'ExecType': '3',
        'OrdStatus': '1',
        'Account': client,
        'Side': 1,
        'Price': price,
        'TimeInForce': 1,
        'ClOrdID': eq_wrappers.get_cl_order_id(base_request),
        'ExecID': '*',
        'LastQty': '*',
        'ExpireDate': '*',
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
        'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'SecondaryOrderID': '*',
        'header': '*',
    }

    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params1, response, message_name='Check params2',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
