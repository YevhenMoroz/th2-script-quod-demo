import time

import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3315"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    client = "MOClient"
    account = "MOClient_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion

    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion

    # region Create DMA
    connectivity_buy_side = test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity()
    rule_manager = RuleManager()
    try:
        rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, client + "_PARIS",
                                                                         "XPAR", int(price))
        trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(connectivity_buy_side, client + "_PARIS", "XPAR",
                                                                       int(price)
                                                                       , int(qty), 0)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
        response = fix_message.pop('response')
        time.sleep(1)
    finally:
        rule_manager.remove_rule(trade_rule)
        rule_manager.remove_rule(rule)
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'BookID': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'AllocInstructionMiscBlock1': '*',
        'BookingType': '*',
        'AllocType': '*',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',

    }
    fix_verifier_bo = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders'])
    # endregion
    # region Approve
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Allocate
    arr_allocation_param = [{"Security Account": account, "Alloc Qty": qty}]
    eq_wrappers.allocate_order(base_request, arr_allocation_param)
    # endregion
    # region Verify
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': qty,
        'AllocAccount': '*',
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'BookID': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'AllocInstructionMiscBlock1': '*',
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
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_bo.CheckConfirmation(params, response, ['AllocAccount', 'NoOrders'])

    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'AllocInstructionMiscBlock1': '*',
        'Currency': '*',
        'BookID': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
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
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': account,
                'AllocPrice': price,
                'AllocQty': qty,
                'NoMiscFees': [
                    {
                        'MiscFeeAmt': '*',
                        'MiscFeeCurr': '*',
                        'MiscFeeType': '*',
                    }
                ]
            }
        ],
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
    # region Un-allocate
    eq_wrappers.unallocate_order(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    # endregion
