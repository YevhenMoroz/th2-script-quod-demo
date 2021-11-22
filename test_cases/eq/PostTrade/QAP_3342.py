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


def execute(report_id,session_id):
    case_name = "QAP-3342"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "3"
    client = "MOClient"
    account1 = "MOClient_SA1"
    account2 = "MOClient_SA2"
    account3 = "MOClient_SA3"
    account4 = "MOClient_SA4"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # # region Create DMA
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client +'_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client +'_PARIS', 'XPAR', int(price),
            int(qty), 1)
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion
    response = fix_message.pop('response')
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # # endregion
    # # region Book
    eq_wrappers.book_order(base_request, client, price)

    # endregion
    time.sleep(1)
    eq_wrappers.approve_block(base_request)
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Accepted')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Matched')
    eq_wrappers.allocate_order(base_request, [{"Security Account": account1, "Alloc Qty": str(int(int(qty)/2))},
                                              {"Security Account": account2, "Alloc Qty": str(int(int(qty)/2))}])
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
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'BookID': 'DMA Washbook',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocInstructionMiscBlock1': '*',
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '0',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier(test_cases.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount','ConfirmTransType'])
    params = {
        # 'Quantity': qty,
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
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'BookID': 'DMA Washbook',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocInstructionMiscBlock1':'*',
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
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
        'BookID': 'DMA Washbook',
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
                'AllocAccount': account1,
                'AllocPrice': price,
                'AllocQty': int(int(qty)/2),
            },
            {
                'AllocNetPrice': '*',
                'AllocAccount': account2,
                'AllocPrice': price,
                'AllocQty':int(int(qty)/2),
            }
        ],
        'AllocInstructionMiscBlock1':'*',
    }
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType','AllocTransType'])

    # region unallocate
    eq_wrappers.unallocate_order(base_request)
    eq_wrappers.allocate_order(base_request, [{"Security Account": account3, "Alloc Qty": str(int(int(qty)/2))},
                                              {"Security Account": account4, "Alloc Qty": str(int(int(qty)/2))}])
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': int(int(qty)/2),
        'AllocAccount': account3,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'BookID': 'DMA Washbook',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'AllocInstructionMiscBlock1':'*',
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
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
    param1 = response.response_messages_list[0].fields['ClOrdID'].simple_value
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AllocInstructionMiscBlock1':'*',
        'AvgPx': '*',
        'AllocQty': int(int(qty)/2),
        'AllocAccount': account4,
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
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookID': 'DMA Washbook',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss.CheckConfirmation(params, response, [param1, 'AllocAccount'])
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
        'BookID': 'DMA Washbook',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '2',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '1',
        'ReportedPx': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': account3,
                'AllocPrice': price,
                'AllocQty': int(int(qty)/2),
            },
            {
                'AllocNetPrice': '*',
                'AllocAccount': account4,
                'AllocPrice': price,
                'AllocQty':int(int(qty)/2),
            }
        ],
        'AllocInstructionMiscBlock1':'*',
    }

    fix_verifier_ss.CheckAllocationInstruction(params, response,
                                               ['NoOrders["ClOrdID"]', 'AllocType', 'Account', 'AllocAccount','AllocTransType'])
