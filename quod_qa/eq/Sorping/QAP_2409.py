import logging
import os
import time
from copy import deepcopy
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID, Message
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 1100
display_qty = 100
price = 45
side = 1
ex_destination_1 = "QL1"
client = "KEPLER"
order_type = "Limit"
case_name = os.path.basename(__file__)
connectivity_feed_handler = "fix-fh-310-columbia"
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
QDL2_id = "9400000038"
QDL1_id = "9400000036"

instrument = {
            'Symbol': "QUODTESTQA00",
            'SecurityID': "TESTQA00",
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1'
        }

def rule_creation():
    rule_manager = RuleManager()
    ioc_rule_1 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, "KEPLER", "QDD1", False, qty, price)
    ioc_rule_2 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, "KEPLER", "QDD2", False, qty, price)
    ioc_rule_3 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, "KEPLER", "QDL2", True, 1000, 40)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "KEPLER", "QDL1", 45)
    trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(connectivity_buy_side, "KEPLER", "QDL1", 45, 100, 0)

    return [nos_rule, ioc_rule_1, ioc_rule_2, ioc_rule_3, trade_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def send_MD(symbol: str, case_id :str, market_data ):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_feed_handler)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_feed_handler,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_feed_handler)
    ))

def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    rule_list = rule_creation()
    market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '44',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            }
        ]
    send_MD(QDL1_id, case_id, market_data1)
    market_data2 = [
        {
            'MDEntryType': '0',
            'MDEntryPx': '28',
            'MDEntrySize': '1000',
            'MDEntryPositionNo': '1'
        },
        {
            'MDEntryType': '1',
            'MDEntryPx': '40',
            'MDEntrySize': '1000',
            'MDEntryPositionNo': '1'
        }
    ]
    send_MD(QDL2_id, case_id, market_data2)
    fix_manager_310 = FixManager(connectivity_sell_side, case_id)
    verifier_310_sell_side = FixVerifier(connectivity_sell_side, case_id)
    verifier_310_buy_side = FixVerifier(connectivity_buy_side, case_id)



    # Send NewOrderSingle
    case_id_1 = bca.create_event("Algo order creation", case_id)
    new_order_single_params = {
        'Account': client,
        'HandlInst': 2,
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': 0,
        'Price': price,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': 1011,
        'ClientAlgoPolicyID': 'QA_SORPING'
    }
    fix_message_new_order_single = FixMessage(new_order_single_params)
    fix_message_new_order_single.add_random_ClOrdID()
    responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)
#
#
#     #Check that FIXQUODSELL5 receive 35=D
#     nos_1 = dict(
#         fix_message_new_order_single.get_parameters(),
#         TransactTime='*',
#         ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))
#
#     verifier_310_sell_side.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL5 receive 35=D')
#
#     #Check that FIXQUODSELL5 sent 35=8 pending new
#     er_1 = dict(
#         ExecID='*',
#         OrderQty=qty,
#         LastQty=0,
#         TransactTime='*',
#         Side=side,
#         AvgPx=0,
#         Currency='EUR',
#         TimeInForce=0,
#         HandlInst =2,
#         LeavesQty=qty,
#         CumQty=0,
#         LastPx=0,
#         OrdType=2,
#         ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'),
#         OrderCapacity='A',
#         QtyType=0,
#         Price=price,
#         TargetStrategy=1011,
#         ExecType="A",
#         OrdStatus='A',
#         OrderID=responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
#         Instrument='*',
#         NoParty='*'
#     )
#
#     verifier_310_sell_side.CheckExecutionReport(er_1, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 pending new')
#
#     #Check that FIXQUODSELL5 sent 35=8 new
#     er_2 = dict(
#         er_1,
#         ExecType="0",
#         OrdStatus='0',
#         SettlDate='*',
#         ExecRestatementReason='*',
#         SettlType='*',
#     )
#     verifier_310_sell_side.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 new')
#
#
#     # Check that algo ping QDD1
#     case_id_2 = bca.create_event("Dark phase", case_id)
#     nos_2 = {
#         'Side': side,
#         'Price': price,
#         'ExDestination': 'QDD1',
#         'Account': client,
#         'OrderQty': qty,
#         'OrdType': 2,
#         'ClOrdID': '*',
#         'OrderCapacity': 'A',
#         'TransactTime': '*',
#         'ChildOrderID': '*',
#         'SettlDate': '*',
#         'Currency': 'EUR',
#         'TimeInForce': 3,
#         'Instrument': '*',
#         'HandlInst': 1
#     }
#     verifier_310_buy_side.CheckNewOrderSingle(nos_2, responce_new_order_single,key_parameters = ['ExDestination', 'Side', 'Price'], case=case_id_2, message_name='Algo ping QDD1' )
#
#     # Check that algo ping QDD2
#     nos_3 = dict(
#         nos_2,
#         ExDestination ='QDD2'
#     )
#     verifier_310_buy_side.CheckNewOrderSingle(nos_3, responce_new_order_single,key_parameters = ['ExDestination', 'Side', 'Price'], case=case_id_2, message_name='Algo ping QDD1')
#
#     # Check that sim cancel IOC order on QDD1
#     er_3 = {
#         'Side': side,
#         # 'Price': price,
#         # 'ExDestination': 'QDD1',
#         # 'Account': client,
#         'ExecID': '*',
#         'OrderQty': qty,
#         'AvgPx': 0,
#         'OrdStatus': 4,
#         'OrdType': 2,
#         'ClOrdID': '*',
#         # 'OrderCapacity': 'A',
#         'TransactTime': '*',
#         # 'ChildOrderID': '*',
#         'TimeInForce': 3,
#         'ExecType': 4,
#         'LeavesQty': 0,
#         'CumQty': 0,
#         'Text': '*',
#         'OrderID': '*'
#     }
#     verifier_310_buy_side.CheckExecutionReport(er_3, responce_new_order_single,key_parameters = ['Side', 'ExecType'], direction='SECOND',case=case_id_2, message_name='ExecutionReport from QDD2')
#
# #TODO Add difference between cancel on QDD1 and QDD2
#
#     # Check that sim cancel IOC order on QDD2
#     er_3 = {
#         'Side': side,
#         # 'Price': price,
#         # 'ExDestination': 'QDD1',
#         # 'Account': client,
#         'ExecID': '*',
#         'OrderQty': qty,
#         'AvgPx': 0,
#         'OrdStatus': 4,
#         'OrdType': 2,
#         'ClOrdID': '*',
#         # 'OrderCapacity': 'A',
#         'TransactTime': '*',
#         # 'ChildOrderID': '*',
#         'TimeInForce': 3,
#         'ExecType': 4,
#         'LeavesQty': 0,
#         'CumQty': 0,
#         'Text': '*',
#         'OrderID': '*'
#     }
#     verifier_310_buy_side.CheckExecutionReport(er_3, responce_new_order_single, key_parameters=['Side', 'ExecType'], direction='SECOND', case=case_id_2, message_name='ExecutionReport from QDD2')
#
#
#     # Check that algo send dday order on QUODLIT1
#
#     case_id_3 = bca.create_event("Lit phase", case_id)
#
#     nos_4 = dict(
#         nos_2,
#         ExDestination ='QDL1',
#         TimeInForce = 0
#     )
#     verifier_310_buy_side.CheckNewOrderSingle(nos_4, responce_new_order_single,key_parameters = ['ExDestination', 'Side', 'Price'], case=case_id_3, message_name='NewOrderSingle to QDL1')
#
#
#     time.sleep(2)
#     er_4 = {
#         'ExDestination': 'QDL1',
#         'ExecType': 'A',
#         'OrdStatus': 'A',
#         'Account': client,
#         'CumQty': 0,
#         'ExecID': '*',
#         'OrderQty': qty,
#         'OrdType': 2,
#         'ClOrdID': '*',
#         'Text': '*',
#         'OrderID': '*',
#         'TransactTime': '*',
#         'Side': side,
#         'AvgPx': 0,
#         'Price': price,
#         'TimeInForce': 0,
#         'LeavesQty': 0
#     }
#     verifier_310_buy_side.CheckExecutionReport(er_4, responce_new_order_single,key_parameters = ['ExDestination', 'ExecType', 'OrdStatus'],direction='SECOND', case=case_id_3, message_name='ExecutionReport pending new')
#
#     er_5 = dict(
#         er_4,
#         ExecType='A',
#         OrdStatus='A',
#     )
#     verifier_310_buy_side.CheckExecutionReport(er_5, responce_new_order_single,key_parameters = ['ExDestination', 'ExecType', 'OrdStatus'],direction='SECOND', case=case_id_3, message_name='ExecutionReport new')
#
#     case_id_4 = bca.create_event("Cancel algo", case_id)
#
#     # Cancel order
#     cancel_parms = {
#         "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
#         "Account": fix_message_new_order_single.get_parameter('Account'),
#         "Side": fix_message_new_order_single.get_parameter('Side'),
#         "TransactTime": datetime.utcnow().isoformat(),
#         "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
#     }
#     fix_cancel = FixMessage(cancel_parms)
#     responce_cancel = fix_manager_310.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_4)
#     cancel_er_params = {
#         'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
#         'OrdStatus': '4',
#         'ExecID': '*',
#         'OrderQty': qty,
#         'LastQty': 0,
#         'OrderID':responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
#         'TransactTime': '*',
#         'Side': side,
#         'AvgPx': 0,
#         'SettlDate': '*',
#         'Currency': 'EUR',
#         'TimeInForce': 0,
#         'ExecType': 4,
#         'HandlInst': 2,
#         'LeavesQty': 0,
#         'NoParty': '*',
#         'CumQty': 0,
#         'LastPx': 0,
#         'OrdType': 2,
#         'OrderCapacity': 'A',
#         'QtyType': 0,
#         'ExecRestatementReason': 4,
#         'SettlType': 0,
#         'Price': price,
#         'TargetStrategy': 1011,
#         'Instrument': '*',
#         'OrigClOrdID': '*'
#     }
#     time.sleep(1)
#     verifier_310_sell_side.CheckExecutionReport(cancel_er_params, responce_cancel, case=case_id_4)
#
#

    time.sleep(10)
    rule_destroyer(rule_list)

