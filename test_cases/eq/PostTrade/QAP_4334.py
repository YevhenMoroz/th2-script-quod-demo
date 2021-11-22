from datetime import timedelta, datetime

import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4334"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "4"
    client = "MOClient2"
    account1 = "MOClient2_SA1"
    base_request = get_base_request(session_id, case_id)
    no_allocs = [
        {
            'AllocAccount': account1,
            'AllocQty': qty
        }
    ]
    # endregion
    # region Create order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', float(price),
            int(qty), 1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price, no_allocs)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion

    # region Verify
    fix_verifier_bo = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    params = {
        'TradeDate': datetime.strftime(datetime.now(), "%Y%m%d"),
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': qty,
        'AllocAccount': account1,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'BookID': '*',
        'header': '*',
        'AllocInstructionMiscBlock1': '*',
        'SettlDate': '*',
        'SettlType': '*',
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
        'ConfirmTransType': '0',
        'ConfirmID': '*'
    }
    fix_verifier_bo.CheckConfirmation(params, response, ['AllocAccount'])
    params = {
        'Quantity': qty,
        'TradeDate': datetime.strftime(datetime.now(), "%Y%m%d"),
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
        'SettlType': '*',
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
        'AllocTransType': '0',
        'ReportedPx': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': account1,
                'AllocPrice': '*',
                'AllocQty': qty,
            }
        ],
        'AllocInstructionMiscBlock1': '*'

    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType', 'AllocTransType'])
    # endregion
