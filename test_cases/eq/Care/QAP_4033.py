import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
import time

from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4033"
    # region Declarations

    qty = "1111"
    price = "40"
    lookup = "VETO"
    client_for_first_order = "CLIENT_VSKULINEC"
    client_for_second_order = "MOClient"
    type_order = 'Limit'
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion

    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client_for_first_order, 2, qty, 0,
                                                                          price)
    response = fix_message.pop('response')
    eq_wrappers.accept_order(lookup, qty, price)
    # region set Disclose Flag
    eq_wrappers.set_disclose_flag_via_order_book(base_request, [1], True)
    # endregion

    # region split order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_fix_wrappers.get_buy_connectivity(),
                                                                             client_for_first_order + '_PARIS', 'XPAR',
                                                                             float(price))
        trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_fix_wrappers.get_buy_connectivity(),
                                                                       client_for_first_order + '_PARIS', 'XPAR',
                                                                       float(price), int(qty), delay=0)
        eq_wrappers.split_order(base_request, qty, type_order, price)

    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(trade_rule)

    # endregion
    # endregion for first order

    # region action with second order
    fix_message_second_order = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2,
                                                                                       client_for_second_order, 2, qty, 0,
                                                                                       price)
    eq_wrappers.scroll_order_book(base_request, count=3)
    response_second_order = fix_message_second_order.pop('response')
    eq_wrappers.accept_order(lookup, qty, price)

    # region set Disclose Flag
    eq_wrappers.set_disclose_flag_via_order_book(base_request, [1], True)
    # endregion

    # region split order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_fix_wrappers.get_buy_connectivity(),
                                                                             client_for_second_order + '_PARIS', 'XPAR',
                                                                             float(price))
        trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_fix_wrappers.get_buy_connectivity(),
                                                                       client_for_second_order + '_PARIS', 'XPAR',
                                                                       float(price), int(qty), delay=0)
        eq_wrappers.split_order(base_request, qty, type_order, price)

    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(trade_rule)
    # endregion
    # endregion second order

    # region execution summary by average_price
    eq_wrappers.mass_execution_summary(base_request, 2, 50)
    #
    params = {
        'OrderQty': qty,
        'ExecType': 'B',
        'Account': client_for_first_order,
        'OrdStatus': 'B',
        'Side': 2,
        'Price': price,
        'TimeInForce': 0,
        'Expire Date': '*',
        'VenueType' : 'O',
        'ExecDestination': 'XPAR',
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
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
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'GrossTradeAmt': '*'
    }

    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType'], direction='FIRST')

    params['Account'] = client_for_second_order
    params['ClOrdID'] = response_second_order.response_messages_list[0].fields['ClOrdID'].simple_value
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType'], direction='FIRST')
