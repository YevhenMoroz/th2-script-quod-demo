import logging
import os
import time
from copy import deepcopy
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import convert_to_request, message_to_grpc
from test_cases.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_cases.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

#order param
qty = 1000
time_in_force = 6
time_in_force_new = 0
price = 35
side = 1
ord_type = 2

#venue param
account = "CLIENT1"
symbol_paris = "734"
symbol_trqx = "3416"

instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

connectivity_buy_side = "fix-bs-310-columbia"
connectivity_feed_handler = "fix-fh-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"

logger = logging.getLogger(__name__)

def rule_creation():
    rule_manager = RuleManager()
    nos_rule_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price)
    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)
    ocr_rule_1 = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", True)
    return [nos_rule_1, ocrr_rule, ocr_rule_1]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def send_market_data(symbol: str, case_id: str, market_data):
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
        # region Send marketData
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
        # endregion
        # region Send NewOrderSingle
        case_id_2 = bca.create_event("Send NewOrderSingle", case_id)
        timenow = datetime.utcnow()
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
            'ExpireDate': (timenow + timedelta(days=2)).strftime("%Y%m%d"),
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
                    'StrategyParameterName': 'UniversalTIF',
                    'StrategyParameterType': '13',
                    'StrategyParameterValue': 'false'
                }
            ]
        }

        fix_message_multilisting = FixMessage(multilisting_params)
        fix_message_multilisting.add_random_ClOrdID()
        responce = fix_manager.Send_NewOrderSingle_FixMessage(fix_message_multilisting, case=case_id_2)

        # Check that FIXQUODSELL5 receive 35=D
        nos_1 = dict(
            fix_message_multilisting.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_multilisting.get_parameter('ClOrdID'))

        verifier_310_sell_side.CheckNewOrderSingle(nos_1, responce, direction='SECOND', case=case_id_2,
                                                   message_name='FIXQUODSELL5 receive 35=D')

        # Check that FIXQUODSELL5 sent 35=8 pending new
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
            TargetStrategy=fix_message_multilisting.get_parameter('TargetStrategy'),
            ExecType="A",
            OrdStatus='A',
            OrderID=responce.response_messages_list[0].fields['OrderID'].simple_value,
            Instrument='*',
            NoParty='*',
            NoStrategyParameters='*',
            ExpireDate=(timenow + timedelta(days=2)).strftime("%Y%m%d")
        )

        verifier_310_sell_side.CheckExecutionReport(er_1, responce, case=case_id_2,
                                                    message_name='FIXQUODSELL5 sent 35=8 pending new')

        # Check that FIXQUODSELL5 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            ExecRestatementReason='*',
            SettlType='*',
        )
        verifier_310_sell_side.CheckExecutionReport(er_2, responce, case=case_id_2,
                                                    message_name='FIXQUODSELL5 sent 35=8 new')
        # endregion
        # region Check buy-side
        time.sleep(2)
        case_id_3 = bca.create_event("Check buy-side", case_id)
        nos_2 = {
            'Side': side,
            'ExDestination': 'XPAR',
            'Account': "XPAR_CLIENT1",
            'OrderQty': qty,
            'OrdType': ord_type,
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
            'ExpireDate': (timenow + timedelta(days=2)).strftime("%Y%m%d"),
            'Price': price
        }
        verifier_310_buy_side.CheckNewOrderSingle(nos_2, responce, key_parameters=['ExDestination', 'Side', 'OrdType'],
                                                  case=case_id_3, message_name='Algo sent child to Paris')

        er_3 = {
            'ExDestination': 'XPAR',
            'ExecType': 'A',
            'OrdStatus': 'A',
            'Account': "XPAR_CLIENT1",
            'CumQty': 0,
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': ord_type,
            'ClOrdID': '*',
            'Text': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': 0,
            'TimeInForce': time_in_force,
            'LeavesQty': 0,
            'Price': price,
            'ExpireDate': (timenow + timedelta(days=2)).strftime("%Y%m%d")
        }
        verifier_310_buy_side.CheckExecutionReport(er_3, responce,
                                                   key_parameters=['ExDestination', 'ExecType', 'OrdStatus',
                                                                   'OrderQty'],
                                                   direction='SECOND', case=case_id_3,
                                                   message_name='ExecutionReport pending new')

        er_4 = dict(
            er_3,
            ExecType='0',
            OrdStatus='0',
        )
        verifier_310_buy_side.CheckExecutionReport(er_4, responce,
                                                   key_parameters=['ExDestination', 'ExecType', 'OrdStatus',
                                                                   'OrderQty'],
                                                   direction='SECOND', case=case_id_3,
                                                   message_name='ExecutionReport new')
        # endregion
        # region Modification message
        case_id_4 = bca.create_event("Modify algo order", case_id)
        fix_modify_message = deepcopy(fix_message_multilisting)
        fix_modify_message.change_parameters({'TimeInForce': time_in_force_new})
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_modify_message.remove_tag('ExpireDate')
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_4)

        ocrr_1 = {
            'Side': side,
            'Account': account,
            'OrderQty': qty,
            'OrdType': ord_type,
            'ClOrdID': fix_message_multilisting.get_ClOrdID(),
            'OrigClOrdID': fix_message_multilisting.get_ClOrdID(),
            'OrderCapacity': 'A',
            'TransactTime': '*',
            'Currency': 'EUR',
            'TimeInForce': time_in_force_new,
            'Instrument': '*',
            'HandlInst': multilisting_params['HandlInst'],
            'Price': price,
            'TargetStrategy': multilisting_params['TargetStrategy'],
            'NoStrategyParameters': '*',
        }
        verifier_310_sell_side.CheckOrderCancelReplaceRequest(ocrr_1, responce, key_parameters=['OrigClOrdID', 'OrdType', 'TimeInForce'],
                                                  case=case_id_4, message_name='Check that sell-side receive 35=G', direction='SECOND')

        ocrr_2 = {
            'Side': side,
            'ExDestination': 'XPAR',
            'Account': "XPAR_CLIENT1",
            'OrderQty': qty,
            'OrdType': ord_type,
            'ClOrdID': '*',
            'OrigClOrdID': '*',
            'OrderCapacity': 'A',
            'TransactTime': '*',
            'Currency': 'EUR',
            'TimeInForce': time_in_force_new,
            'Instrument': '*',
            'HandlInst': 1,
            'Price': price,
            'ChildOrderID': '*',
            'OrderID': '*',
            'NoParty': '*'

        }
        verifier_310_buy_side.CheckOrderCancelReplaceRequest(ocrr_2, responce, key_parameters=['Account', 'ExDestination', 'OrdType', 'TimeInForce'],
                                                  case=case_id_4, message_name='Check that Quod send 35=G')

        time.sleep(2)


        er_5 = {
            # 'ExDestination': 'XPAR',
            'ExecType': '5',
            'OrdStatus': '0',
            # 'Account': "XPAR_CLIENT1",
            'CumQty': 0,
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': ord_type,
            'ClOrdID': '*',
            'Text': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': 0,
            'TimeInForce': time_in_force_new,
            'LeavesQty': 1000,
            'Price': price,
            'OrigClOrdID': '*'
        }
        verifier_310_buy_side.CheckExecutionReport(er_5, responce,
                                                   key_parameters=['ExecType', 'OrdStatus',
                                                                   'OrderQty'],
                                                   direction='SECOND', case=case_id_4,
                                                   message_name='ExecutionReport replaced')
        time.sleep(1)

        # Check that FIXQUODSELL5 sent 35=8 pending new
        er_6 = dict(
            ExecID='*',
            OrderQty=qty,
            LastQty=0,
            TransactTime='*',
            Side=side,
            AvgPx=0,
            Currency='EUR',
            TimeInForce=time_in_force_new,
            HandlInst=2,
            LeavesQty=qty,
            CumQty=0,
            LastPx=0,
            OrdType=ord_type,
            ClOrdID=fix_message_multilisting.get_parameter('ClOrdID'),
            OrderCapacity='A',
            QtyType=0,
            Price=price,
            TargetStrategy=fix_message_multilisting.get_parameter('TargetStrategy'),
            ExecType="5",
            OrdStatus='0',
            OrderID=responce.response_messages_list[0].fields['OrderID'].simple_value,
            Instrument='*',
            NoParty='*',
            NoStrategyParameters='*',
            SettlDate='*',
            ExecRestatementReason='4',
            SettlType='0',
            OrigClOrdID='*'
        )

        verifier_310_sell_side.CheckExecutionReport(er_6, responce, case=case_id_4, key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'],
                                                    message_name='FIXQUODSELL5 sent 35=8 replaced')

        # endregion
        # region Cancel order
        case_id_4 = bca.create_event("Cancel order", case_id)
        cancel_parms = {
            "ClOrdID": fix_message_multilisting.get_ClOrdID(),
            "Account": fix_message_multilisting.get_parameter('Account'),
            "Side": fix_message_multilisting.get_parameter('Side'),
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": fix_message_multilisting.get_ClOrdID()
        }
        fix_cancel = FixMessage(cancel_parms)
        responce_cancel = fix_manager.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_4)
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
            'TimeInForce': 0,
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
            'NoStrategyParameters': '*'
        }
        verifier_310_sell_side.CheckExecutionReport(cancel_er_params, responce_cancel, case=case_id_4)
        # endregion
        rule_destroyer(rule_list)
    except Exception:
        logging.error("Error execution", exc_info=True)