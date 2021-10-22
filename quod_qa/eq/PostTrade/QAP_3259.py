import quod_qa.wrapper.eq_fix_wrappers
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


def execute(report_id, session_id):
    case_name = "QAP-3259"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "3"
    client = "MOClient"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client +'_PARIS', "XPAR", 3)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client +'_PARIS', 'XPAR', 3,
            800, 1)
        time.sleep(5)
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion
    response = fix_message.pop('response')
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # # endregion
    # # region Book
    responce1 = eq_wrappers.book_order(base_request, client, price,
                                       misc_arr=['amendClient1', 'amendClient2', 'amendClient3',
                                                 'amendClient4', 'amendClient5'])
    # endregion
    time.sleep(10)
    # region Verify
    params = {
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
        'GrossTradeAmt': '*',
        'NoRootMiscFeesList': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocInstructionMiscBlock1' : {
            'BOMiscField3':'amendClient3',
            'BOMiscField4':'amendClient5',
            'BOMiscField1': 'amendClient2',
            'BOMiscField2': 'amendClient3',
            'BOMiscField0': 'amendClient1'
        },
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '*',
        # 'RootSettlCurrAmt': '*',
        'RootOrClientCommission': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'RootOrClientCommissionCurrency': '*',
        'RootCommTypeClCommBasis': '*',
        'RootSettlCurrAmt': '*'

    }
    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    # endregion
    # region aprrove block
    eq_wrappers.approve_block(base_request)

    responce2 = eq_wrappers.allocate_order(base_request, [{"Security Account": "MOClientSA1", "Alloc Qty": "800",
                                                           'Alloc BO Field 1': 'amendAccount1',
                                                           'Alloc BO Field 2': 'amendAccount2',
                                                           'Alloc BO Field 3': 'amendAccount3',
                                                           'Alloc BO Field 4': 'amendAccount4',
                                                           'Alloc BO Field 5': 'amendAccount5'}]
                                           )
    # endregion
    time.sleep(10)
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': 800,
        'AllocAccount': '*',
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
        'AllocInstructionMiscBlock1': {
            'BOMiscField3': 'amendClient3',
            'BOMiscField4': 'amendClient5',
            'BOMiscField1': 'amendClient2',
            'BOMiscField2': 'amendClient3',
            'BOMiscField0': 'amendClient1'
        },
        'AllocInstructionMiscBlock2': {
            'BOMiscField7': 'amendAccount3',
            'BOMiscField8': 'amendAccount4',
            'BOMiscField5': 'amendAccount1',
            'BOMiscField6': 'amendAccount2',
            'BOMiscField9': 'amendAccount5'
        },
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
        'CommissionData': '*',
        'NoMiscFees': '*',
        'ConfirmID': '*'
    }

    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders'])
    params = {
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
        'GrossTradeAmt': '*',
        # 'NoMiscFees': '*',
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
        # 'RootOrClientCommission': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': 'MOClientSA1',
                'AllocPrice': '3',
                'AllocQty': qty,
                'ComissionData': {
                    'CommissionType': '*',
                    'Commission': '*',
                    'CommCurrency': '*'
                },
                'NoMiscFees': [
                    {
                        'MiscFeeAmt': '*',
                        'MiscFeeCurr': '*',
                        'MiscFeeType': '*',
                    }
                ]
            }
        ],

        # 'RootOrClientCommissionCurrency': '*',
        # 'RootCommTypeClCommBasis': '*'

    }
    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
