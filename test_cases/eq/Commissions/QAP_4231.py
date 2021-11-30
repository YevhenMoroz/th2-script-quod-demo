import time

import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.eq_wrappers import open_fe

from win_gui_modules.utils import get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4231"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_COMM_1"
    account = "CLIENT_COMM_1_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    no_allocs = [
        {
            'AllocAccount': account,
            'AllocQty': qty
        }
    ]
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create Orders
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            float(price), int(qty), 1)

        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 2, client, 2, qty, 0, price, no_allocs)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    eq_wrappers.book_order(base_request, client, price)
    eq_wrappers.approve_block(base_request)
    eq_wrappers.allocate_order(base_request)
    # region Verify
    params = {
        'OrderQty': qty,
        'ExecType': 'F',
        'Account': '*',
        'OrdStatus': 2,
        'TradeDate': '*',
        'Side': 2,
        'ExpireDate': '*',
        'Price': price,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'LastExecutionPolicy': '*',
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
        'header': '*',
        'SecondaryExecID': '*',
        'Text': '*',
        'SecondaryOrderID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params1',
                                         key_parameters=['ClOrdID', 'OrdStatus'])
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'Account': client,
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '5',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'AllocInstructionMiscBlock1': '*',
    }
    fix_verifier_bo = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': qty,
        'AllocAccount': account,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'CommissionData':
            {'CommissionType': '3',
             'Commission': '45',
             'CommCurrency': 'EUR'},
        'AllocInstructionMiscBlock1': '*',
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_bo.CheckConfirmation(params, response, ['NoOrders'])
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'Account': client,
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '9.95',
                'AllocAccount': account,
                'AllocPrice': '10',
                'AllocQty': qty,
                'CommissionData': {
                    'CommissionType': '3',
                    'CommCurrency': 'EUR',
                    'Commission': '45'}
            }
        ],
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '2',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'AllocInstructionMiscBlock1': '*',
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
