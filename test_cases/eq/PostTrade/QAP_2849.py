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
    case_name = "QAP-2849"
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
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
                                                                             'MOClient_PARIS', "XPAR", 3)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(), 'MOClient_PARIS', 'XPAR', 3,
            800, 1)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
        response = fix_message.pop('response')
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    #
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # # endregion
    #
    # # region Book
    eq_wrappers.book_order(base_request, client, price)
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
        # 'SettlType': 0,
        'GrossTradeAmt': '*',
        'NoRootMiscFeesList': '*',
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
        'RootOrClientCommission': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'RootOrClientCommissionCurrency': '*',
        'RootCommTypeClCommBasis': '*'

    }
    fix_verifier_ss = FixVerifier('fix-ss-back-office', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    # endregion
    # region aprrove block
    eq_wrappers.approve_block(base_request)
    # endregion
    time.sleep(10)
    params = {
        # 'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': 900,
        'AllocAccount': '*',
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        # 'SettlType': '0',
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
        # 'AllocTransType': '0',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        # 'RootOrClientCommissionCurrency': '*',
        'CommissionData': '*',
        'NoMiscFees': '*',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-ss-back-office', case_id)
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
        # 'SettlType': 0,
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
                'AllocPrice': '40',
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
    fix_verifier_ss = FixVerifier('fix-ss-back-office', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
