import test_cases.wrapper.eq_fix_wrappers
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from test_cases.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4471"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "4"
    client = "MOClient4"
    account1 = "MOClient4_SA1"
    account2 = "MOClient4_SA2"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    no_allocs = [
        {
            'AllocAccount': account1,
            'AllocQty': int(qty) / 2
        },
        {
            'AllocAccount': account2,
            'AllocQty': int(qty) / 2
        }
    ]
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', float(price),
            int(qty), 1)
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price, no_allocs)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion
    # # region check order at order book
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # endregion

    # region book
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region Verify
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'Booked', False)
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'ApprovalPending')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Unmatched')
    # endregion
    # region approve block
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Accepted')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Matched')
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': int(int(qty)/2),
        'AllocAccount': account1,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'BookID': '*',
        'header': '*',
        'AllocInstructionMiscBlock1': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '0',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier(test_cases.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['AllocAccount'])
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': int(int(qty)/2),
        'AllocAccount': account2,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'BookID': '*',
        'header': '*',
        'AllocInstructionMiscBlock1': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '0',
        'ConfirmID': '*'
    }
    fix_verifier_ss.CheckConfirmation(params, response, ['AllocAccount'])
    # endregion
