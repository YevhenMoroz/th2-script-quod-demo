import logging
import os
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs


qty = 1000
qty_xpar = 300
qty_trqx = 700
account = "CLIENT1"
time_in_force = 0
price = 35
side = 1
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_feed_handler = "fix-fh-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
symbol_paris = "734"
symbol_trqx = "3416"
ord_type = 2
instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }


def rule_creation():
    rule_manager = RuleManager()
    nos_rule_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price)
    nos_rule_2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "TRQX_CLIENT1", "TRQX", price)
    ocr_rule_1 = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", True)
    ocr_rule_2 = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "TRQX_CLIENT1", "TRQX", True)
    return [nos_rule_1, nos_rule_2, ocr_rule_1, ocr_rule_2]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)

def send_market_data(symbol: str, case_id :str, market_data ):
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
    try:
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        rule_list = rule_creation()
        fix_manager = FixManager(connectivity_sell_side, case_id)
        verifier_310_sell_side = FixVerifier(connectivity_sell_side, case_id)
        verifier_310_buy_side = FixVerifier(connectivity_buy_side, case_id)

        case_id_1 = bca.create_event("Send MarketData", case_id)
        market_data1 = [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '30',
                    'MDEntrySize': '100000',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '40',
                    'MDEntrySize': '100000',
                    'MDEntryPositionNo': '1'
                }
            ]
        send_market_data(symbol_paris, case_id_1, market_data1)
        market_data2 = [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '30',
                    'MDEntrySize': '100000',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '40',
                    'MDEntrySize': '100000',
                    'MDEntryPositionNo': '1'
                }
            ]
        send_market_data(symbol_trqx, case_id_1, market_data2)


        # Send NewOrderSingle
        case_id_2 = bca.create_event("Send NewOrderSingle", case_id)

        multilisting_params = {
            'Account': account,
            'HandlInst': "2",
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': time_in_force,
            'Price': price,
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
                },
                {
                    'StrategyParameterName': 'PostMode',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'Spraying'
                },
                {
                    'StrategyParameterName': 'VenueWeights',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'TRQX=7/PARIS=3'
                }
            ]
        }

        fix_message_multilisting = FixMessage(multilisting_params)
        fix_message_multilisting.add_random_ClOrdID()
        responce = fix_manager.Send_NewOrderSingle_FixMessage(fix_message_multilisting, case=case_id_2)


        #Check that FIXQUODSELL5 receive 35=D
        nos_1 = dict(
            fix_message_multilisting.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_multilisting.get_parameter('ClOrdID'))

        verifier_310_sell_side.CheckNewOrderSingle(nos_1, responce, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 receive 35=D')

        #Check that FIXQUODSELL5 sent 35=8 pending new
        er_1 = dict(
            ExecID='*',
            OrderQty=qty,
            LastQty=0,
            TransactTime='*',
            Side=side,
            AvgPx=0,
            Currency='EUR',
            TimeInForce=time_in_force,
            HandlInst =2,
            LeavesQty=qty,
            CumQty=0,
            LastPx=0,
            OrdType=2,
            ClOrdID=fix_message_multilisting.get_parameter('ClOrdID'),
            OrderCapacity='A',
            QtyType=0,
            Price=price,
            TargetStrategy=fix_message_multilisting.get_parameter('TargetStrategy'),
            ExecType="A",
            OrdStatus='A',
            OrderID=responce.response_messages_list[0].fields['OrderID'].simple_value,
            Instrument='*',
            NoParty='*',
            NoStrategyParameters='*'
        )

        verifier_310_sell_side.CheckExecutionReport(er_1, responce, case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 pending new')

        #Check that FIXQUODSELL5 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            ExecRestatementReason='*',
        )
        verifier_310_sell_side.CheckExecutionReport(er_2, responce, case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 new')



        # Check buy-side

        # NewOrderSingle on XPAR
        case_id_3 = bca.create_event("Check buy-side on XPAR", case_id)
        nos_2 = {
            'Side': side,
            'Price': price,
            'ExDestination': 'XPAR',
            'Account': "XPAR_CLIENT1",
            'OrderQty': 300,
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
            'NoParty': '*'
        }
        verifier_310_buy_side.CheckNewOrderSingle(nos_2, responce, key_parameters = ['ExDestination', 'Side', 'Price', 'OrderQty'], case=case_id_3 )

        time.sleep(5)
        # Execution Report pending
        er_4 = {
            'ExDestination': 'XPAR',
            'ExecType': 'A',
            'OrdStatus': 'A',
            'Account': 'XPAR_CLIENT1',
            'CumQty': 0,
            'ExecID': '*',
            'OrderQty': 300,
            'OrdType': 2,
            'ClOrdID': '*',
            'Text': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': 0,
            'Price': price,
            'TimeInForce': time_in_force,
            'LeavesQty': qty_xpar
        }
        verifier_310_buy_side.CheckExecutionReport(er_4, responce,
                                                   key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty'],
                                                   direction='SECOND', case=case_id_3,
                                                   message_name='ExecutionReport pending new')

        er_5 = dict(
            er_4,
            ExecType='0',
            OrdStatus='0',
        )
        verifier_310_buy_side.CheckExecutionReport(er_5, responce,
                                                   key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty'],
                                                   direction='SECOND', case=case_id_3, message_name='ExecutionReport new')

        # NewOrderSingle on TRQX
        case_id_3 = bca.create_event("Check buy-side on TRQX", case_id)
        nos_3 = {
            'Side': side,
            'Price': price,
            'ExDestination': 'TRQX',
            'Account': "TRQX_CLIENT1",
            'OrderQty': 700,
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
            'NoParty': '*'
        }
        verifier_310_buy_side.CheckNewOrderSingle(nos_3, responce,
                                                  key_parameters=['ExDestination', 'Side', 'Price', 'OrderQty'],
                                                  case=case_id_3)

        time.sleep(5)
        # Execution Report pending
        er_6 = {
            'ExDestination': 'TRQX',
            'ExecType': 'A',
            'OrdStatus': 'A',
            'Account': 'TRQX_CLIENT1',
            'CumQty': 0,
            'ExecID': '*',
            'OrderQty': 700,
            'OrdType': 2,
            'ClOrdID': '*',
            'Text': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': 0,
            'Price': price,
            'TimeInForce': time_in_force,
            'LeavesQty': qty_trqx
        }
        verifier_310_buy_side.CheckExecutionReport(er_6, responce,
                                                   key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty'],
                                                   direction='SECOND', case=case_id_3,
                                                   message_name='ExecutionReport pending new')

        er_7 = dict(
            er_4,
            ExecType='0',
            OrdStatus='0',
        )
        verifier_310_buy_side.CheckExecutionReport(er_7, responce,
                                                   key_parameters=['ExDestination', 'ExecType', 'OrdStatus', 'OrderQty'],
                                                   direction='SECOND', case=case_id_3, message_name='ExecutionReport new')

        case_id_5 = bca.create_event("Cancel order", case_id)
        # Cancel order
        cancel_parms = {
            "ClOrdID": fix_message_multilisting.get_ClOrdID(),
            "Account": account,
            "Side": side,
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": fix_message_multilisting.get_ClOrdID()
        }
        fix_cancel = FixMessage(cancel_parms)
        responce_cancel = fix_manager.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_5)
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
            'Price': price,
            'TargetStrategy': 1008,
            'NoStrategyParameters': '*',
            'Instrument': '*',
            'OrigClOrdID': '*'
        }
        time.sleep(1)
        verifier_310_sell_side.CheckExecutionReport(cancel_er_params, responce_cancel, case=case_id_5)
        time.sleep(2)
        rule_destroyer(rule_list)
    except Exception:
        logging.error("Error execution", exc_info=True)