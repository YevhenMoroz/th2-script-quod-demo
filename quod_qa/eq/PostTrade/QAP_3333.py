import time

import quod_qa.wrapper.eq_fix_wrappers
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3333"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "50"
    client = "MOClient"
    account = "MOClient_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            int(price), int(qty), 1)
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Verify
    fix_verifier_sell = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_sell_connectivity(), case_id)
    params = {
        'Account': client,
        'OrderQty': qty,
        'ExecType': '*',
        'OrdStatus': '2',
        'ExpireDate': '*',
        'Side': 1,
        'Price': price,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'SettlDate': '*',
        'LastExecutionPolicy': '*',
        'TradeDate': '*',
        'LastMkt': '*',
        'SettlType': '*',
        'Text': '*',
        'AvgPx': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'NoParty': '*',
        'Instrument': {
            'SecurityType': 'CS',
            'Symbol': '*',
            'SecurityIDSource': '*',
            'SecurityID': '*',
            'SecurityExchange': '*'
        }
    }
    fix_verifier_sell.CheckExecutionReport(params, response, ['ClOrdID','OrdStatus'])
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    # endregion
    # region Approve
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    # endregion
    # region Allocate
    arr_allocation_param = [{"Security Account": account, "Alloc Qty": qty}]
    eq_wrappers.allocate_order(base_request, arr_allocation_param)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Summary Status", "MatchedAgreed")
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    eq_wrappers.verify_allocate_value(base_request, case_id, "Status", "Affirmed")
    eq_wrappers.verify_allocate_value(base_request, case_id, "Match Status", "Matched")
    fix_verifier_bo = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)

    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'BookID': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'SecondaryOrderID': '*',
        'AllocInstructionMiscBlock1': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '*',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'Instrument': {
            'SecurityDesc': '*',
            'SecurityType': 'CS',
            'Symbol': '*',
            'SecurityIDSource': '*',
            'SecurityID': '*',
            'SecurityExchange': '*'
        }
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders'])
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
        'header': '*',
        'BookID': '*',
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
        'ConfirmTransType': '*',
        'ConfirmID': '*',
        'Instrument': {
            'SecurityDesc': '*',
            'SecurityType': 'CS',
            'Symbol': '*',
            'SecurityIDSource': '*',
            'SecurityID': '*',
            'SecurityExchange': '*'
        }
    }
    fix_verifier_bo.CheckConfirmation(params, response, ['NoOrders'])
    # endregion
