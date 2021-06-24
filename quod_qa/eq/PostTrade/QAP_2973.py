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
    case_name = "QAP-2973"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
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
    # # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-bs-eq-paris',
                                                                             'MOClient_PARIS', "XPAR", 3)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade('fix-bs-eq-paris', 'MOClient_PARIS', 'XPAR', 3,
                                                                      800, 1)
        time.sleep(5)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
        response = fix_message.pop('response')
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # eq_wrappers.accept_order("VETO", qty, price)
    # eq_wrappers.manual_execution(base_request, qty, price)
    # eq_wrappers.complete_order(base_request)
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # # endregion
    #
    # # region Book
    response_book = eq_wrappers.book_order(base_request, client, price, settlement_currency='UAH', exchange_rate='2',
                                           exchange_rate_calc='Multiple', toggle_recompute=True)
    print(response_book)
    # endregion
    time.sleep(10)
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
    fix_verifier_ss = FixVerifier('fix-ss-back-office', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    # endregion
    # region aprrove block
    eq_wrappers.approve_block(base_request)
    # endregion
    param = [{"Security Account": "MOClientSA1", "Alloc Qty": qty}]
    responce_allocation = eq_wrappers.allocate_order(base_request, param)
    print(responce_allocation)
    time.sleep(1)
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
        'ConfirmID': '*',
        'SettlCurrFxRate': '2',
        'SettlCurrFxRateCalc': 'M',
        'SettlCurrency': 'UAH',
        'SettlCurrAmt': str(int(float(responce_allocation['book.netAmount'].replace(',', '')) * 2)).replace(',', '')
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
        # 'SettlCurrFxRate': '2',
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
        # 'RootOrClientCommissionCurrency': '*',
        # 'RootCommTypeClCommBasis': '*'
        'RootSettlCurrFxRate': '2',
        'RootSettlCurrFxRateCalc': 'M'
    }
    fix_verifier_ss = FixVerifier('fix-ss-back-office', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
