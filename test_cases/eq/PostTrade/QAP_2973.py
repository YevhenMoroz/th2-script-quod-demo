import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-2973"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    client = "MOClient"

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    #  endregion
    #  region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', float(price), int(qty),
            1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 1, price)
        time.sleep(1)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        response = fix_message.pop('response')
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    #  endregion
    #  region Book
    response_book = eq_wrappers.book_order(base_request, client, price, settlement_currency='UAH', exchange_rate='2',
                                           exchange_rate_calc='Multiple', toggle_recompute=True)
    # endregion
    # region Verify
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'RootSettlCurrFxRateCalc': 'M',
        'AvgPx': response_book['book.agreedPrice'].replace(',', ''),
        'Side': '*',
        'Currency': 'UAH',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'RootSettlCurrFxRateCalc': 'M',
        'LastMkt': '*',
        # 'SettlType': 0,
        'GrossTradeAmt': response_book['book.grossAmount'].replace(',', ''),
        'NoRootMiscFeesList': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': response_book['book.netAmount'].replace(',', ''),
        'BookingType': '*',
        'AllocType': '*',
        'RootSettlCurrency': 'UAH',
        'RootSettlCurrAmt': response_book['book.netAmount'].replace(',', ''),
        'RootSettlCurrFxRate': 2,
        'RootOrClientCommission': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'RootOrClientCommissionCurrency': '*',
        'RootCommTypeClCommBasis': '*'

    }
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    # endregion
    # region aprrove block
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Verify
    param = [{"Security Account": "MOClientSA1", "Alloc Qty": qty}]
    responce_allocation = eq_wrappers.allocate_order(base_request, param)
    params = {
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
        'CommissionData': '*',
        'NoMiscFees': '*',
        'ConfirmID': '*',
        'SettlCurrFxRate': '2',
        'SettlCurrFxRateCalc': 'M',
        'SettlCurrency': 'UAH',
        'SettlCurrAmt': "*"
    }
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
        'RootSettlCurrFxRateCalc': 'M',

        'ReportedPx': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': 'MOClientSA1',
                'AllocPrice': str(int(float(price) * 2)),
                'AllocQty': qty,
                'AllocSettlCurrAmt': str(int(float(responce_allocation['book.netAmount'].replace(',', '')) * 2)),
                'AllocSettlCurrency': 'UAH',
                'SettlCurrAmt': str(int(float(responce_allocation['book.netAmount'].replace(',', '')) * 2)),
                'SettlCurrFxRate': '2',
                'SettlCurrency': 'UAH',
                'ComissionData': {
                    'CommissionType': '*',
                    'Commission': '*',
                    'CommCurrency': '*'
                },
                'SettlCurrFxRateCalc': 'M',
                'NoMiscFees': [
                    {
                        'MiscFeeAmt': '*',
                        'MiscFeeCurr': '*',
                        'MiscFeeType': '*',
                    }
                ]
            }
        ],
        'RootSettlCurrency': 'UAH',
        'RootSettlCurrFxRate': '2',
        'RootSettlCurrFxRateCalc': 'M'
    }
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
