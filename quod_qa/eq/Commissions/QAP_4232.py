import time

from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event

from win_gui_modules.utils import get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4232"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_FEES_1"
    account = "CLIENT_FEES_1_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    lookup = "VETO"
    no_allocs = [
        {
            'AllocAccount': account,
            'AllocQty': qty
        }
    ]
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create Orders
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price, no_allocs)
    response = fix_message.pop('response')
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    eq_wrappers.manual_execution(base_request, qty, price)
    eq_wrappers.complete_order(base_request)
    eq_wrappers.book_order(base_request, client, price)
    eq_wrappers.approve_block(base_request)
    eq_wrappers.allocate_order(base_request)
    # region Verify
    params = {
        'OrderQty': qty,
        'ExecType': 'A',
        'Account': '*',
        'OrdStatus': 'A',
        'Side': 2,
        'ExpireDate': '*',
        'Price': price,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
    }
    fix_verifier_ss = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params1',
                                         key_parameters=['ClOrdID'])
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
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '5',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'AllocInstructionMiscBlock1': '*',
    }
    fix_verifier_bo = FixVerifier(eq_wrappers.get_bo_connectivity(), case_id)
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
            {
                'MiscFeeAmt': '450',
                'MiscFeeCurr': 'EUR',
                'MiscFeeType': '22'
            }
        ],
        'CommissionData': {
            'Commission': '450'
        },
        'AllocInstructionMiscBlock1': '*',
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_bo.CheckConfirmation(params, response, ['NoOrders'])
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
        'NoAllocs': [
            {
                'AllocNetPrice': '9.5',
                'AllocAccount': account,
                'AllocPrice': '10',
                'AllocQty': qty,
                'NoMiscFees': [
                    {
                        'MiscFeeAmt': '450',
                        'MiscFeeCurr': 'EUR',
                        'MiscFeeType': '22'
                    }]

            },

        ],
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
        'AllocInstructionMiscBlock1': '*',
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
