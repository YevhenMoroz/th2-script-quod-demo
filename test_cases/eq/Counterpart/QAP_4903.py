import logging
import time
from datetime import datetime, timedelta

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4903"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_COUNTERPART"
    # endregion
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        fix_manager = FixManager(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
        fix_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': qty,
            'TimeInForce': 0,
            'OrdType': 2,
            'Price': price,
            'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'TargetStrategy': 1004,
            'Currency': 'EUR',
            "DisplayInstruction": {
                'DisplayQty': int(qty) - 1
            },
        }
        fix_params.update()
        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        response = fix_manager.Send_NewOrderSingle_FixMessage(fix_message)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # region Verify
    params = {
        'ExecType': '0',
        'OrdStatus': '0',
        'Side': 1,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'ExecBroker': '*',
        'NoParty': [
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "32",
             'PartyID': "Custodian - User2",
             'PartyIDSource': "C"},
            {'PartyRole': "36",
             'PartyID': "gtwquod1",
             'PartyIDSource': "D"}
        ],
        'Instrument': '*',
        'MaxFloor': int(qty) - 1,
        'QuodTradeQualifier': '*',
        'ExecRestatementReason': '*',
        'TargetStrategy': '1004',
        'BookID': '*',
        'Price': price,
        'OrderQtyData': {
            'OrderQty': qty
        }
    }
    fix_verifier_bo = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=None)
    # endregion
