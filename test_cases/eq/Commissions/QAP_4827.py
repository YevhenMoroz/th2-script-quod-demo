import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4859"
    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENT_COMM_2"
    account = "CLIENT_COMM_2_SA1"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    instrument = {
        'Symbol': 'IS0000000001_EUR',
        'SecurityID': 'IS0000000001',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XEUR'
    }
    # endregion
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_EUREX', "XEUR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_EUREX', 'XEUR', float(price),
            int(qty), 1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price, instrument)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    param = [{"Security Account": account, "Alloc Qty": qty}
             ]
    eq_wrappers.allocate_order(base_request,param)
    # region Verify
    fix_verifier_bo = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
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
        'SettlType': '*',
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
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'CommissionData': {
            'CommissionType': '*',
            'Commission': '*',
            'CommCurrency': 'EUR'
        },
        'ConfirmID': '*'
    }

    fix_verifier_bo.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
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
        'NoAllocs': [
            {'AllocNetPrice': '*',
             'AllocQty': qty,
             'AllocAccount': account,
             'AllocPrice': price,
             'CommissionData': {
                 'CommissionType': '3',
                 'Commission': '4500',
                 'CommCurrency': 'EUR',
             }
             }
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '2',
        'SettlType': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
