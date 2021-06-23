from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-3342"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "3"
    client = "MOClient"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # # region Create DMA
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-317ganymede-standard',
                                                                             'MO_Client_PARIS', "XPAR", 3)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade('fix-buy-317ganymede-standard',
                                                                      'MO_Client_PARIS', 'XPAR', 3,
                                                                      800, 1)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
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
    eq_wrappers.allocate_order(base_request, [{"Security Account": "MOClient_SA1", "Alloc Qty": "400"},
                                              {"Security Account": "MOClient_SA2", "Alloc Qty": "400"}])
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': 400,
        'AllocAccount': 'MOClient_SA1',
        'ConfirmType': 2,
        'Side': '*',
        'Account': 'MOClient',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        # 'NoRootMiscFeesList': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'BookID': 'DMA Washbook',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocInstructionMiscBlock1':
            {
                'BOMiscField4': 'TH2TH2TH2',
                'BOMiscField3': '4',
                'BOMiscField2': '3',
                'BOMiscField1': '2',
                'BOMiscField0': '1',

            },
        'AllocID': '*',
        'NetMoney': '*',
        # 'BookingType': '*',
        # 'AllocType': '*',
        # 'RootSettlCurrAmt': '*',
        # 'AllocTransType': '1',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        # 'CommissionData': '*',
        # 'NoMiscFees': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': 400,
        'AllocAccount': 'MOClient_SA2',
        'ConfirmType': 2,
        'Side': '*',
        'Account': 'MOClient',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        # 'NoRootMiscFeesList': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'BookID': 'DMA Washbook',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocInstructionMiscBlock1':
            {
                'BOMiscField4': 'TH2TH2TH2',
                'BOMiscField3': '4',
                'BOMiscField2': '3',
                'BOMiscField1': '2',
                'BOMiscField0': '1',

            },
        'AllocID': '*',
        'NetMoney': '*',
        # 'BookingType': '*',
        # 'AllocType': '*',
        # 'RootSettlCurrAmt': '*',
        # 'AllocTransType': '1',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        # 'CommissionData': '*',
        # 'NoMiscFees': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'Account': 'MOClient',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        # 'NoRootMiscFeesList': '*',
        # 'MatchStatus': '*',
        # 'ConfirmStatus': '*',
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
        # 'CpctyConfGrp': '*',
        # 'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        # 'CommissionData': '*',
        # 'NoMiscFees': '*',
        # 'ConfirmID': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': 'MOClient_SA1',
                'AllocPrice': '3',
                'AllocQty': 400,
            },
            {
                'AllocNetPrice': '*',
                'AllocAccount': 'MOClient_SA2',
                'AllocPrice': '3',
                'AllocQty': 400,
            }
        ],
        'AllocInstructionMiscBlock1':
            {
                'BOMiscField4': 'TH2TH2TH2',
                'BOMiscField3': '4',
                'BOMiscField2': '3',
                'BOMiscField1': '2',
                'BOMiscField0': '1',

            },
    }
    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType','AllocTransType'])

    # region unallocate
    eq_wrappers.unallocate_order(base_request)
    eq_wrappers.allocate_order(base_request, [{"Security Account": "MOClient_SA3", "Alloc Qty": "400"},
                                              {"Security Account": "MOClient_SA4", "Alloc Qty": "400"}])
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': 400,
        'Account': 'MOClient',
        'AllocAccount': 'MOClient_SA3',
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
        'AllocInstructionMiscBlock1':
            {
                'BOMiscField4': 'TH2TH2TH2',
                'BOMiscField3': '4',
                'BOMiscField2': '3',
                'BOMiscField1': '2',
                'BOMiscField0': '1',

            },
        # 'NoRootMiscFeesList': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        # 'BookingType': '*',
        # 'AllocType': '*',
        # 'RootSettlCurrAmt': '*',
        # 'AllocTransType': '0',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        # 'CommissionData': '*',
        # 'NoMiscFees': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
    param1 = response.response_messages_list[0].fields['ClOrdID'].simple_value
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AllocInstructionMiscBlock1':
            {
                'BOMiscField4': 'TH2TH2TH2',
                'BOMiscField3': '4',
                'BOMiscField2': '3',
                'BOMiscField1': '2',
                'BOMiscField0': '1',

            },
        'AvgPx': '*',
        'AllocQty': 400,
        'AllocAccount': 'MOClient_SA4',
        'Account': 'MOClient',
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        # 'NoRootMiscFeesList': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        # 'BookingType': '*',
        # 'AllocType': '*',
        # 'RootSettlCurrAmt': '*',
        'BookID': 'DMA Washbook',
        # 'AllocTransType': '1',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        # 'CommissionData': '*',
        # 'NoMiscFees': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckConfirmation(params, response, [param1, 'AllocAccount'])
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'Account': 'MOClient',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        # 'NoRootMiscFeesList': '*',
        # 'MatchStatus': '*',
        # 'ConfirmStatus': '*',
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
        # 'CpctyConfGrp': '*',
        # 'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        # 'CommissionData': '*',
        # 'NoMiscFees': '*',
        # 'ConfirmID': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': 'MOClient_SA3',
                'AllocPrice': '3',
                'AllocQty': 400,
            },
            {
                'AllocNetPrice': '*',
                'AllocAccount': 'MOClient_SA4',
                'AllocPrice': '3',
                'AllocQty': 400,
            }
        ],
        'AllocInstructionMiscBlock1':
            {
                'BOMiscField4': 'TH2TH2TH2',
                'BOMiscField3': '4',
                'BOMiscField2': '3',
                'BOMiscField1': '2',
                'BOMiscField0': '1',

            },
    }

    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response,
                                               ['NoOrders["ClOrdID"]', 'AllocType', 'Account', 'AllocAccount','AllocTransType'])
