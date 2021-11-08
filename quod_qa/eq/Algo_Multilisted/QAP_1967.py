import os
import time
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

#order param
qty = 1300
time_in_force = 0
price_1 = 35
stop_price_1 = 35
price_2 = 34
stop_price_2 = 34
price_3 = 36
stop_price_3 = 36
side = 1

#venue param
account = "CLIENT1"
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_feed_handler = "fix-fh-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
symbol_paris = "734"
symbol_trqx = "3416"
ord_type = 4
instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_rule_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price_1)
    nos_rule_2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price_2)
    nos_rule_3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price_3)
    occr_rule = rule_manager.add_OCRR(connectivity_buy_side)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", True)
    return [nos_rule_1, nos_rule_2, nos_rule_3, occr_rule, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def send_md(case_id):
    MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="734",
        connection_id=ConnectionID(session_alias=connectivity_feed_handler)
    )).MDRefID

    mdir_params_trade = {
        'MDReqID': MDRefID_1,
        'NoMDEntriesIR': [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '38.5',
                'MDEntrySize': '3000',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    }
    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh', connectivity_feed_handler, case_id,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, connectivity_feed_handler)
    ))
    time.sleep(10)
    mdir_params_trade = {
        'MDReqID': MDRefID_1,
        'NoMDEntriesIR': [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '38.5',
                'MDEntrySize': '3000',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    }
    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh', connectivity_feed_handler, case_id,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, connectivity_feed_handler)
    ))



def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    fix_manager = FixManager(connectivity_sell_side, case_id)
    fix_verifier_sell_side = FixVerifier(connectivity_sell_side, case_id)
    fix_verifier_buy_side = FixVerifier(connectivity_buy_side, case_id)

    list_rules = rule_creation()




    # Send NewOrderSingle
    case_id_1 = bca.create_event("Create algo order", case_id)
    multilisting_params = {
        'Account': account,
        'HandlInst': "2",
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': time_in_force,
        'StopPx': stop_price_1,
        'Price': price_1,
        'OrdType': ord_type,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1008",
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'AvailableVenues',
                'StrategyParameterType': '13',
                'StrategyParameterValue': 'true'
            },
            {
                'StrategyParameterName': 'AllowMissingPrimary',
                'StrategyParameterType': '13',
                'StrategyParameterValue': 'true'
            }
        ]
    }

    fix_message_multilisting = FixMessage(multilisting_params)
    fix_message_multilisting.add_random_ClOrdID()
    responce = fix_manager.Send_NewOrderSingle_FixMessage(fix_message_multilisting, case=case_id_1)
    time.sleep(1)

    # Check that FIXQUODSELL5 receive 35=8 pending new
    er_1 = dict(
        Account=account,
        ExecID='*',
        OrderQty=qty,
        LastQty=0,
        TransactTime='*',
        Side=side,
        AvgPx=0,
        Currency='EUR',
        TimeInForce=0,
        HandlInst=2,
        LeavesQty=qty,
        CumQty=0,
        LastPx=0,
        OrdType=ord_type,
        ClOrdID=fix_message_multilisting.get_parameter('ClOrdID'),
        OrderCapacity='A',
        QtyType=0,
        Price=price_1,
        TargetStrategy=1008,
        ExecType="A",
        OrdStatus='A',
        OrderID=responce.response_messages_list[0].fields['OrderID'].simple_value,
        Instrument='*',
        NoParty='*',
        StopPx=stop_price_1,
        NoStrategyParameters='*'
    )

    fix_verifier_sell_side.CheckExecutionReport(er_1, responce, case=case_id_1,
                                                message_name='FIXQUODSELL5 sent 35=8 pending new')

    # Check that FIXQUODSELL5 receive 35=8 new
    er_2 = dict(
        er_1,
        ExecType="0",
        OrdStatus='0',
        SettlDate='*',
        ExecRestatementReason='*',
    )
    er_2.pop('Account')
    fix_verifier_sell_side.CheckExecutionReport(er_2, responce, case=case_id_1,
                                                message_name='FIXQUODSELL5 sent 35=8 new')

    time.sleep(5)
    # Send MD
    case_id_2 = bca.create_event("MarketData send", case_id)
    send_md(case_id_2)

    # Check buy-side
    case_id_3 = bca.create_event("Check buy-side", case_id)
    nos_2 = {
        'Side': side,
        'Price': stop_price_1,
        'ExDestination': 'XPAR',
        'Account': "XPAR_CLIENT1",
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'OrderCapacity': 'A',
        'TransactTime': '*',
        'SettlDate': '*',
        'Currency': 'EUR',
        'TimeInForce': 0,
        'Instrument': '*',
        'HandlInst': 1,
        'NoParty': '*'
    }
    fix_verifier_buy_side.CheckNewOrderSingle(nos_2, responce, key_parameters=['ExDestination', 'Side', 'Price'],
                                              case=case_id_3, message_name='Stop algo sent child to venue')

    er_3 = {
        'ExDestination': 'XPAR',
        'ExecType': 'A',
        'OrdStatus': 'A',
        'Account': "XPAR_CLIENT1",
        'CumQty': 0,
        'ExecID': '*',
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'Text': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': 0,
        'Price': stop_price_1,
        'TimeInForce': 0,
        'LeavesQty': qty
    }
    fix_verifier_buy_side.CheckExecutionReport(er_3, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty', 'Price'],
                                               direction='SECOND', case=case_id_3,
                                               message_name='ExecutionReport pending new')

    er_4 = dict(
        er_3,
        ExecType='A',
        OrdStatus='A',
    )
    fix_verifier_buy_side.CheckExecutionReport(er_4, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty', 'Price'],
                                               direction='SECOND', case=case_id_3, message_name='ExecutionReport new')

    # Send OrderCancelReplaceRequest `First modification`
    case_id_4 = bca.create_event("First modification", case_id)
    fix_modify_message = deepcopy(fix_message_multilisting)
    fix_modify_message.change_parameters({'Price': price_2, 'StopPx': stop_price_2})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_4)

    # Check on  (FIXSELLQUOD5 35=G)
    replace_ss_param = {
        'Account': account,
        'OrderQty': qty,
        'OrdType': ord_type,
        'NoStrategyParameters': '*',
        'TransactTime': '*',
        'Side': side,
        'Currency': "EUR",
        'TimeInForce': time_in_force,
        'Instrument': instrument,
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'Price': price_2,
        'StopPx': stop_price_2,
        'TargetStrategy': multilisting_params['TargetStrategy'],
        'OrigClOrdID': fix_message_multilisting.get_ClOrdID(),
        'HandlInst': 2
    }
    fix_verifier_sell_side.CheckOrderCancelReplaceRequest(replace_ss_param, responce, direction='SECOND',
                                                   case=case_id_4, message_name='TH2 send 35=G Replace',
                                                   key_parameters=['TimeInForce', 'OrderQty', 'Price', 'ClOrdID',
                                                                   'OrigClOrdID'])


    time.sleep(5)
    # Send MD
    case_id_5 = bca.create_event("MarketData send", case_id)
    send_md(case_id_5)


    # Check buy-side
    case_id_6 = bca.create_event("Check buy-side", case_id)
    nos_2 = {
        'Side': side,
        'Price': stop_price_2,
        'ExDestination': 'XPAR',
        'Account': "XPAR_CLIENT1",
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'OrderCapacity': 'A',
        'TransactTime': '*',
        'SettlDate': '*',
        'Currency': 'EUR',
        'TimeInForce': 0,
        'Instrument': '*',
        'HandlInst': 1,
        'NoParty': '*'
    }
    fix_verifier_buy_side.CheckNewOrderSingle(nos_2, responce, key_parameters=['ExDestination', 'Side', 'Price'],
                                              case=case_id_6, message_name='Stop algo sent child to venue')

    er_3 = {
        'ExDestination': 'XPAR',
        'ExecType': 'A',
        'OrdStatus': 'A',
        'Account': "XPAR_CLIENT1",
        'CumQty': 0,
        'ExecID': '*',
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'Text': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': 0,
        'Price': stop_price_2,
        'TimeInForce': 0,
        'LeavesQty': qty
    }
    fix_verifier_buy_side.CheckExecutionReport(er_3, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty', 'Price'],
                                               direction='SECOND', case=case_id_6,
                                               message_name='ExecutionReport pending new')

    er_4 = dict(
        er_3,
        ExecType='A',
        OrdStatus='A',
    )
    fix_verifier_buy_side.CheckExecutionReport(er_4, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty', 'Price'],
                                               direction='SECOND', case=case_id_6, message_name='ExecutionReport new')

    # Send OrderCancelReplaceRequest `Second modification`
    case_id_7 = bca.create_event("Second modification", case_id)
    fix_modify_message = deepcopy(fix_message_multilisting)
    fix_modify_message.change_parameters({'Price': price_3, 'StopPx': stop_price_3})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_7)
    time.sleep(2)

    # Send MarketData
    case_id_8 = bca.create_event("MarketData send", case_id)
    send_md(case_id_8)

    time.sleep(2)
    # Check buy-side
    case_id_9 = bca.create_event("Check buy-side", case_id)
    nos_2 = {
        'Side': side,
        'Price': stop_price_3,
        'ExDestination': 'XPAR',
        'Account': "XPAR_CLIENT1",
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'OrderCapacity': 'A',
        'TransactTime': '*',
        'SettlDate': '*',
        'Currency': 'EUR',
        'TimeInForce': 0,
        'Instrument': '*',
        'HandlInst': 1,
        'NoParty': '*'
    }
    fix_verifier_buy_side.CheckNewOrderSingle(nos_2, responce, key_parameters=['ExDestination', 'Side', 'Price'],
                                              case=case_id_9, message_name='Stop algo sent child to venue')

    er_3 = {
        'ExDestination': 'XPAR',
        'ExecType': 'A',
        'OrdStatus': 'A',
        'Account': "XPAR_CLIENT1",
        'CumQty': 0,
        'ExecID': '*',
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'Text': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': 0,
        'Price': stop_price_3,
        'TimeInForce': 0,
        'LeavesQty': qty
    }
    fix_verifier_buy_side.CheckExecutionReport(er_3, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty', 'Price'],
                                               direction='SECOND', case=case_id_9,
                                               message_name='ExecutionReport pending new')

    er_4 = dict(
        er_3,
        ExecType='A',
        OrdStatus='A',
    )
    fix_verifier_buy_side.CheckExecutionReport(er_4, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty', 'Price'],
                                               direction='SECOND', case=case_id_9, message_name='ExecutionReport new')
    # Cancel order
    case_id_10 = bca.create_event("Cancel order", case_id)
    cancel_parms = {
        "ClOrdID": fix_message_multilisting.get_ClOrdID(),
        "Account": fix_message_multilisting.get_parameter('Account'),
        "Side": fix_message_multilisting.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_multilisting.get_ClOrdID()
    }
    fix_cancel = FixMessage(cancel_parms)
    time.sleep(2)
    responce_cancel = fix_manager.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_10)
    cancel_er_params = {
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrdStatus': '4',
        'ExecID': '*',
        'OrderQty': qty,
        'LastQty': 0,
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': 0,
        'SettlDate': '*',
        'Currency': 'EUR',
        'TimeInForce': time_in_force,
        'ExecType': 4,
        'HandlInst': 2,
        'LeavesQty': 0,
        'NoParty': '*',
        'CumQty': 0,
        'LastPx': 0,
        'OrdType': ord_type,
        'OrderCapacity': 'A',
        'QtyType': 0,
        'ExecRestatementReason': 4,
        'Price': price_3,
        'TargetStrategy': 1008,
        'Instrument': '*',
        'OrigClOrdID': '*',
        'StopPx': stop_price_3,
        'NoStrategyParameters': '*'
    }
    fix_verifier_sell_side.CheckExecutionReport(cancel_er_params, responce_cancel, case=case_id_10,key_parameters = ['ClOrdID', 'OrdStatus','StopPx', 'Price'])

    time.sleep(2)
    rule_destroyer(list_rules)