import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3338"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "3"
    client = "MOClient"
    account1 = "MOClient_SA1"
    account2 = "MOClient_SA2"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # # endregion
    # # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", 3)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', int(price), int(qty),
            1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price)
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
    eq_wrappers.book_order(base_request, client, price, misc_arr=['BOF1C', 'BOF2C', 'BOF3C',
                                                                  'BOF4C', 'BOF5C'])
    # endregion
    # region Verify
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
        'GrossTradeAmt': '*',
        'BookID': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocInstructionMiscBlock1': {
            'BOMiscField3': 'BOF4C',
            'BOMiscField4': 'BOF5C',
            'BOMiscField1': 'BOF2C',
            'BOMiscField2': 'BOF3C',
            'BOMiscField0': 'BOF1C'
        },
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'RootSettlCurrAmt': '*'

    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    # endregion
    # region aprrove block
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Allocate
    eq_wrappers.allocate_order(base_request, [{"Security Account": account1, "Alloc Qty": str(int(int(qty) / 2)),
                                               'Alloc BO Field 1': 'BOF1A1',
                                               'Alloc BO Field 2': 'BOF2A1',
                                               'Alloc BO Field 3': 'BOF3A1',
                                               'Alloc BO Field 4': 'BOF4A1',
                                               'Alloc BO Field 5': 'BOF5A1'},
                                              {"Security Account": account2, "Alloc Qty": str(int(int(qty) / 2)),
                                               'Alloc BO Field 1': 'BOF1A2',
                                               'Alloc BO Field 2': 'BOF2A2',
                                               'Alloc BO Field 3': 'BOF3A2',
                                               'Alloc BO Field 4': 'BOF4A2',
                                               'Alloc BO Field 5': 'BOF5A2'}]
                               )
    # endregion
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': str(int(int(qty) / 2)),
        'AllocAccount': account1,
        'ConfirmType': 2,
        'Side': '*',
        'BookID': '*',
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
        'AllocInstructionMiscBlock1': {
            'BOMiscField4': 'BOF5C',
            'BOMiscField3': 'BOF4C',
            'BOMiscField2': 'BOF3C',
            'BOMiscField1': 'BOF2C',
            'BOMiscField0': 'BOF1C'
        },
        'AllocInstructionMiscBlock2': {
            'BOMiscField5': 'BOF1A1',
            'BOMiscField6': 'BOF2A1',
            'BOMiscField7': 'BOF3A1',
            'BOMiscField8': 'BOF4A1',
            'BOMiscField9': 'BOF5A1'
        },
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }

    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': str(int(int(qty) / 2)),
        'AllocAccount': account2,
        'ConfirmType': 2,
        'Side': '*',
        'BookID': '*',
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
        'AllocInstructionMiscBlock1': {
            'BOMiscField4': 'BOF5C',
            'BOMiscField3': 'BOF4C',
            'BOMiscField2': 'BOF3C',
            'BOMiscField1': 'BOF2C',
            'BOMiscField0': 'BOF1C'
        },
        'AllocInstructionMiscBlock2': {
            'BOMiscField5': 'BOF1A2',
            'BOMiscField6': 'BOF2A2',
            'BOMiscField7': 'BOF3A2',
            'BOMiscField8': 'BOF4A2',
            'BOMiscField9': 'BOF5A2'
        },
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }

    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders', 'AllocAccount'])

    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'BookID': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'AllocInstructionMiscBlock1': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'},
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
                'AllocQty': int(int(qty) / 2),
                'AllocInstructionMiscBlock2':
                    {
                        'BOMiscField7': 'BOF3A1',
                        'BOMiscField8': 'BOF4A1',
                        'BOMiscField5': 'BOF1A1',
                        'BOMiscField6': 'BOF2A1',
                        'BOMiscField9': 'BOF5A1',
                    }
            },
            {
                'AllocNetPrice': '*',
                'AllocAccount': account2,
                'AllocPrice': price,
                'AllocQty': int(int(qty) / 2),
                'AllocInstructionMiscBlock2':
                    {
                        'BOMiscField7': 'BOF3A2',
                        'BOMiscField8': 'BOF4A2',
                        'BOMiscField5': 'BOF1A2',
                        'BOMiscField6': 'BOF2A2',
                        'BOMiscField9': 'BOF5A2',
                    }


            }
        ]
    }
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
