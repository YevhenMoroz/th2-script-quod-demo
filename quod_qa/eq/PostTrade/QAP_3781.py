import time

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
    case_name = "QAP-3770"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "49540"
    price = "0.789"
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
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                      client + '_PARIS', 'XPAR',
                                                                      float(price), int(qty), 1)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price, comm_basis="Percent", comm_rate="0.1", fees_basis="Absolute",
                           fees_rate="1", fees_type="Tax")
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    params = {
        'Account': client,
        'Quantity': qty,
        'RootCommTypeClCommBasis': '3',
        'RootOrClientCommission': '*',
        'RootOrClientCommissionCurrency': '*',
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'BookID': '*',
        'NoParty': '*',
        'NoRootMiscFeesList': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'AllocInstructionMiscBlock1': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '38680.84',
        'BookingType': '*',
        'AllocType': '5',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',

    }
    fix_verifier_bo = FixVerifier(eq_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
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
    params = {
        # 'Quantity': qty,
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
        'NoMiscFees': [
            {'MiscFeeAmt': '1',
             'MiscFeeCurr': '*',
             'MiscFeeType': '2'}
        ],
        'AllocInstructionMiscBlock1': '*',
        'CommissionData': {
            'CommissionType': '3',
            'CommCurrency': '*',
            'Commission': '38.64'},
        'AllocID': '*',
        'NetMoney': '38680.84',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
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
        'AllocID': '*',
        'NetMoney': '38680.84',
        'BookingType': '*',
        'AllocType': '2',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',

        'NoAllocs': [
            {
                'AllocNetPrice': '0.78',
                'AllocAccount': account,
                'AllocPrice': '0.78',
                'AllocQty': qty,
                'NoMiscFees': [
                    {'MiscFeeAmt': '1',
                     'MiscFeeCurr': '*',
                     'MiscFeeType': '2'}]
                ,
                'CommissionData': {
                    'CommissionType': '3',
                    'CommCurrency': '*',
                    'Commission': '38.64'}
            }
        ],
        'AllocInstructionMiscBlock1': '*',
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType', 'AllocTransType'])
    # endregion