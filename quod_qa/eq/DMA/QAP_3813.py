import logging
import time
from datetime import datetime
from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest
from custom import basic_custom_actions as bca
import quod_qa.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_fix_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.wrappers import set_base
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3813"
    # region Declarations
    qty = "900"
    client = "CLIENT1"
    price = '40'
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    # endregion
    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_fix_wrappers.get_buy_connectivity(),
                                                                             'XPAR_' + client, 'XPAR', float(price))
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # region JavaApi Amend
    act_java_api = Stubs.act_java_api
    connectivity = '317_java_api'
    params = {
        'SEND_SUBJECT': 'QUOD.ORS.FE',
        'OrderModificationRequestBlock': {
            'CounterpartList': {
                'CounterpartBlock': [{'PartyRole': 'GiveupClearingFirm',
                                      'CounterpartID': '200005'}]
            },
            'OrdID': response.response_messages_list[0].fields['OrderID'].simple_value,
            'OrdType': 'LMT',
            'Price': price + '.000000000',
            'TimeInForce': 'DAY',
            'PositionEffect': 'O',
            'OrdQty': qty + '.000000000',
            'OrdCapacity': 'A',
            'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            'MaxPriceLevels': '1',
            'BookingType': 'TRS',
            'RouteID': '24',
            'ExecutionPolicy': 'D',
            'AccountGroupID': client,
            'WashBookAccountID': "DefaultWashBook"
        }
    }
    try:
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(eq_fix_wrappers.get_buy_connectivity(),
                                                               'XPAR_' + client, "XPAR", True)
        act_java_api.sendMessage(request=ActJavaSubmitMessageRequest(
            message=bca.message_to_grpc('Order_OrderModificationRequest', params, connectivity),
            parent_event_id=case_id))
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(ocrr_rule)
    # endregion
    # region Check values in OrderBook
    params = {
        'ReplyReceivedTime': '*',
        'Account': client,
        'OrderQty': qty,
        'Price': price,
        'ExecType': '5',
        'OrdStatus': '0',
        'Side': 1,
        'TimeInForce': 0,
        'OrigClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ClOrdID': '*',
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'Currency': '*',
        'Text': 'order replaced',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SecondaryOrderID': '*',
        'NoParty': [{'PartyRole': "14",
                     'PartyID': "GiveupClearingFirm",
                     'PartyIDSource': "C"},
                    {'PartyRole': "38",
                     'PartyID': "PositionAccount - DMA Washbook",
                     'PartyIDSource': "C"}
                    ],
        'Instrument': '*',
        'SettlType': '0'
    }
    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, ['OrigClOrdID', 'ExecType'])
    # endregion
