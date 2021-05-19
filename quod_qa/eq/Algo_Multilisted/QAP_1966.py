import os
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

qty = 2000
account = "CLIENT1"
time_in_force = 6
price = 35
stop_price = 33
side = 1
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
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", True)
    return [nos_rule, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager = FixManager(connectivity_sell_side, case_id)
    fix_verifier_sell_side = FixVerifier(connectivity_sell_side, case_id)
    fix_verifier_buy_side = FixVerifier(connectivity_buy_side, case_id)

    list_rules = rule_creation()



    case_id_1 = bca.create_event("Create algo order", case_id)
    case_id_2 = bca.create_event("Send MarketData", case_id)
    case_id_3 = bca.create_event("Check buy-side", case_id)
    case_id_4 = bca.create_event("Cancel order", case_id)

    # Send NewOrderSingle
    multilisting_params = {
        'Account': account,
        'HandlInst': "2",
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': time_in_force,
        'StopPx': stop_price,
        'Price': price,
        'OrdType': ord_type,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1008",
        'ExpireDate': (datetime.today() + timedelta(days=2)).strftime("%Y%m%d"),
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
    # Check Execution reports on sell-side

    # Check that FIXQUODSELL5 receive 35=8 pending new
    er_1 = dict(
        ExecID='*',
        OrderQty=qty,
        LastQty=0,
        TransactTime='*',
        Side=side,
        AvgPx=0,
        Currency='EUR',
        TimeInForce=time_in_force,
        HandlInst=2,
        LeavesQty=qty,
        CumQty=0,
        LastPx=0,
        OrdType=ord_type,
        ClOrdID=fix_message_multilisting.get_parameter('ClOrdID'),
        OrderCapacity='A',
        QtyType=0,
        Price=price,
        TargetStrategy=1008,
        ExecType="A",
        OrdStatus='A',
        OrderID=responce.response_messages_list[0].fields['OrderID'].simple_value,
        Instrument='*',
        NoParty='*',
        StopPx=stop_price,
        NoStrategyParameters='*',
        ExpireDate=fix_message_multilisting.get_parameter('ExpireDate')
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
        SettlType='*',
    )
    fix_verifier_sell_side.CheckExecutionReport(er_2, responce, case=case_id_1,
                                                message_name='FIXQUODSELL5 sent 35=8 new')

    time.sleep(5)
    # Send MD

    MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="734",
        connection_id=ConnectionID(session_alias="fix-fh-310-columbia")
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
        'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_2,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
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
        'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_2,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
    ))





    time.sleep(2)
    # Check buy-side
    nos_2 = {
        'Side': side,
        'Price': price,
        'ExDestination': 'XPAR',
        'Account': "XPAR_CLIENT1",
        'OrderQty': qty,
        'OrdType': 2,
        'ClOrdID': '*',
        'OrderCapacity': 'A',
        'TransactTime': '*',
        'ChildOrderID': '*',
        'SettlDate': '*',
        'Currency': 'EUR',
        'TimeInForce': time_in_force,
        'Instrument': '*',
        'HandlInst': 1,
        'NoParty': '*',
        'ExpireDate': (datetime.today() + timedelta(days=2)).strftime("%Y%m%d")
    }
    fix_verifier_buy_side.CheckNewOrderSingle(nos_2, responce,key_parameters = ['ExDestination', 'Side', 'Price'], case=case_id_3, message_name='Stop algo sent child to venue')

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
        'Price': price,
        'TimeInForce': time_in_force,
        'LeavesQty': 0
    }
    fix_verifier_buy_side.CheckExecutionReport(er_3, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus','OrderQty'],
                                               direction='SECOND', case=case_id_3,
                                               message_name='ExecutionReport pending new')

    er_4 = dict(
        er_3,
        ExecType='A',
        OrdStatus='A',
    )
    fix_verifier_buy_side.CheckExecutionReport(er_4, responce,
                                               key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty'],
                                               direction='SECOND', case=case_id_3, message_name='ExecutionReport new')

    # Cancel order
    cancel_parms = {
        "ClOrdID": fix_message_multilisting.get_ClOrdID(),
        "Account": fix_message_multilisting.get_parameter('Account'),
        "Side": fix_message_multilisting.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_multilisting.get_ClOrdID()
    }
    fix_cancel = FixMessage(cancel_parms)
    responce_cancel = fix_manager.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_4)


    time.sleep(3)
    cancel_er_params = {
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrdStatus': '4',
        'ExecID': '*',
        'OrderQty': qty,
        'LastQty': 0,
        'OrderID':responce.response_messages_list[0].fields['OrderID'].simple_value,
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
        'SettlType': 0,
        'Price': price,
        'TargetStrategy': 1008,
        'Instrument': '*',
        'OrigClOrdID': '*',
        'StopPx': stop_price,
        'NoStrategyParameters': '*',
        'ExpireDate': (datetime.today() + timedelta(days=2)).strftime("%Y%m%d")
    }
    fix_verifier_sell_side.CheckExecutionReport(cancel_er_params, responce_cancel, case=case_id_4)

    rule_destroyer(list_rules)