import os
import logging
import time
from datetime import datetime
from copy import deepcopy
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 1200
venue_qty = 400
text_pn='Pending New status'
text_n='New status'
text_ocrr='OCRRRule'
text_c='order canceled'
text_f='Fill'
price = 23
agr_price = 20
side = 2
tif_ioc = 3
ex_destination_1 = "XPAR"
ex_destination_2 = 'TRQX'
client = "CLIENT2"
order_type = "Limit"
account = 'XPAR_CLIENT2'
account2 = 'TRQX_CLIENT2'
currency = 'EUR'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'

instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, agr_price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    nos1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account2, ex_destination_2, True, 800, agr_price)
    nos2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, venue_qty, 21)
    return [nos1_rule, nos2_rule, ocr_rule, nos1_ioc_rule, nos2_ioc_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def execute(report_id):

    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="734",
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    mdir_params_bid = {
        'MDReqID': MDRefID,
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '21',
                'MDEntrySize': '400',
                'MDEntryPositionNo': '1'
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        report_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_fh)
    ))

    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="3416",
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    mdir_params_bid = {
        'MDReqID': MDRefID,
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '20',
                'MDEntrySize': '400',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '22',
                'MDEntrySize': '400',
                'MDEntryPositionNo': '1'
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        report_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_fh)
    ))


    rule_list = rule_creation();
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    # Send_MarkerData
    fix_manager_310 = FixManager(connectivity_sell_side, case_id)
    fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
    fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
    

    #region Send NewOrderSingle (35=D)
    case_id_1 = bca.create_event("Create Algo Order", case_id)
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
        'Currency': currency,
        'TargetStrategy': 1008,
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
    fix_message_new_order_single = FixMessage(new_order_single_params)
    fix_message_new_order_single.add_random_ClOrdID()
    responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)

    #Check that FIXQUODSELL5 receive 35=D
    nos_1 = dict(
        fix_message_new_order_single.get_parameters(),
        TransactTime='*',
        ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

    fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL5 receive 35=D')

   
    #Check that FIXQUODSELL5 sent 35=8 pending new
    er_1 ={
        'ExecID': '*',
        'OrderQty': qty,
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': 'A',
        'Currency': currency,
        'TimeInForce': new_order_single_params['TimeInForce'],
        'ExecType': "A",
        'HandlInst': new_order_single_params['HandlInst'],
        'LeavesQty': qty,
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': new_order_single_params['OrdType'],
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(), 
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'Price': price,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument

    }
    fix_verifier_ss.CheckExecutionReport(er_1, responce_new_order_single, case=case_id_1,   message_name='FIXQUODSELL5 sent 35=8 Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

    # Check that FIXQUODSELL5 sent 35=8 new
    er_2 = dict(
        er_1,
        ExecType="0",
        OrdStatus='0',
        SettlDate='*',
        ExecRestatementReason='*',
        SettlType='*',
    )
    fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
    #endregion

    #region Check Buy Side
    case_id_2 = bca.create_event("Check Buy Side", case_id)
    # Check bs (FIXQUODSELL5 sent 35=D pending new)
    new_order_single_bs = {
        'NoParty': '*',
        'Account': account,        
        'OrderQty': qty,
        'OrdType': new_order_single_params['OrdType'],
        'ClOrdID': '*',
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'TransactTime': '*',
        'ChildOrderID': '*',
        'Side': side,
        'Price': price,
        'SettlDate': '*',
        'Currency': currency,
        'TimeInForce': new_order_single_params['TimeInForce'],
        'Instrument': '*',
        'HandlInst': '1',
        'ExDestination': instrument['SecurityExchange']
    }
    fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce_new_order_single, case=case_id_2, message_name='BS FIXBUYTH2 sent 35=D New order')

    # Check that FIXBUYQUOD5 sent 35=8 pending new
    er_3 = {
        'Account': account,
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': qty,
        'Text': text_pn,
        'OrdType': '2',
        'ClOrdID': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': 'A',
        'Price': price,
        'TimeInForce': new_order_single_params['TimeInForce'],
        'ExecType': "A",
        'ExDestination': ex_destination_1,
        'LeavesQty': '0'
    }

    fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 Pending New', key_parameters=['ExecType', 'OrdStatus'])

    # Check that FIXBUYQUOD5 sent 35=8 new
    er_4 = dict(
        er_3,
        OrdStatus='0',
        ExecType="0",
        OrderQty=qty,
        Text=text_n,
    )
    fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])
    #endregion

    #region Modify order
    case_id_3 = bca.create_event("Modify Order", case_id)
    # Send OrderCancelReplaceRequest  
    fix_modify_message = deepcopy(fix_message_new_order_single)
    fix_modify_message.change_parameters({'Price': agr_price})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_3)

    time.sleep(3)

    # Check SS (FIXSELLQUOD5 35=G)
    replace_ss_param = {
        'Account': client,
        'OrderQty': qty,
        'OrdType': new_order_single_params['OrdType'],
        'NoStrategyParameters': new_order_single_params['NoStrategyParameters'],
        'TransactTime': '*',
        'Side': side,
        'Currency': currency,
        'TimeInForce': '0',
        'Instrument': instrument,
        'HandlInst': new_order_single_params['HandlInst'],
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'Price': agr_price,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'OrigClOrdID': fix_message_new_order_single.get_ClOrdID(),
    }
    fix_verifier_ss.CheckOrderCancelReplaceRequest(replace_ss_param, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='SS FIXSELLQUOD5 sent 35=G Replace',key_parameters=['OrderQty', 'Price', 'ClOrdID',  'OrigClOrdID'])

    # Check BS (FIXBUYTH2 35=8 on 35=F)
    er_5 = {
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': qty,
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'ClOrdID': '*',
        'Text': text_c,
        'OrigClOrdID': '*'
    }
    fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='BS FIXSELLQUOD5 sent 35=8 Replace',key_parameters=['OrderQty', 'OrdStatus', 'ExecType'])

    # Check ss replace order 35=8 on 35=G
    er_6 = {
        'ExecID': '*',
        'OrderQty': qty,
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '*',
        'Currency': currency,
        'TimeInForce': '0',
        'ExecType': '5',
        'HandlInst': new_order_single_params['HandlInst'],
        'LeavesQty': qty,
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': new_order_single_params['OrdType'],
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': agr_price,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument,
        'OrigClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'OrdStatus': '0'
    }

    fix_verifier_ss.CheckExecutionReport(er_6, responce_new_order_single, case=case_id_3, message_name='SS FIXSELLQUOD5 sent 35=8 Replace',key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])
    #endregion

    #region Agro Order
    case_id_4 = bca.create_event("Agro Order", case_id)
    # Check new order TRQX Turquoise qty 800 price 20
    # Check that FIXBUYQUOD5 sent 35=8 pending new
    er_7 = {
        'Account': account2,
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': qty - venue_qty,
        'Text': text_pn,
        'OrdType': '2',
        'ClOrdID': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': 'A',
        'Price': agr_price,
        'TimeInForce': tif_ioc,
        'ExecType': "A",
        'ExDestination': ex_destination_2,
        'LeavesQty': qty - venue_qty
    }

    fix_verifier_bs.CheckExecutionReport(er_7, responce_new_order_single, direction='SECOND', case=case_id_4, message_name='FIXQUODSELL5 sent 35=8 Pending New TRQX', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])


    # Check new order XPAR Paris qty 400 price 21
    # Check that FIXBUYQUOD5 sent 35=8 pending new
    er_8 = {
        'Account': account,
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': venue_qty,
        'Text': text_pn,
        'OrdType': '2',
        'ClOrdID': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': 'A',
        'Price': 21,
        'TimeInForce': tif_ioc,
        'ExecType': "A",
        'ExDestination': ex_destination_1,
        'LeavesQty': venue_qty
    }

    fix_verifier_bs.CheckExecutionReport(er_8, responce_new_order_single, direction='SECOND', case=case_id_4, message_name='FIXQUODSELL5 sent 35=8 Pending New Paris', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

    # Check that FIXBUYQUOD5 sent 35=8 new
    er_9 = dict(
        er_7,
        OrdStatus='0',
        ExecType="0",
        OrderQty=qty - venue_qty,
        Text=text_n,
        LeavesQty=qty - venue_qty,
        Account=account2,
        ExDestination=ex_destination_2
    )
    fix_verifier_bs.CheckExecutionReport(er_9, responce_new_order_single, direction='SECOND', case=case_id_4,  message_name='FIXQUODSELL5 sent 35=8 New TRQX', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])

    # Check that FIXBUYQUOD5 sent 35=8 new
    er_10 = dict(
        er_8,
        OrdStatus='0',
        ExecType="0",
        OrderQty=venue_qty,
        Text=text_n,
        LeavesQty=venue_qty
    )
    fix_verifier_bs.CheckExecutionReport(er_10, responce_new_order_single, direction='SECOND', case=case_id_4,  message_name='FIXQUODSELL5 sent 35=8 New Paris', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])
    #endregion

    #region Filled Order
    case_id_5 = bca.create_event("Fill Order", case_id)
    #Check BS (FIXBUYTH2 TRQX 35=8 Filled)
    er_11 = {
        'Account': account2,
        'CumQty': qty - venue_qty,
        'LastPx': agr_price,
        'ExecID': '*',
        'OrderQty': qty - venue_qty,
        'OrdType': '2',
        'ClOrdID': '*',
        'LastQty': qty - venue_qty,
        'Text': text_f,
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '*',
        'OrdStatus': '2',
        'Price': agr_price,
        'Currency': currency,
        'TimeInForce': tif_ioc,
        'Instrument': '*',
        'ExecType': "F",
        'ExDestination': ex_destination_2,
        'LeavesQty': '0'
    }
    time.sleep(2)
    fix_verifier_bs.CheckExecutionReport(er_11, responce_new_order_single, direction='SECOND', case=case_id_5,  message_name='BS FIXBUYTH2 sent 35=8 Filled Turquoise', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus', 'TimeInForce'])

    #Check BS (FIXBUYTH2 Paris 35=8 Filled)
    er_12 = {
        'Account': account,
        'CumQty': venue_qty,
        'LastPx': 21,
        'ExecID': '*',
        'OrderQty': venue_qty,
        'OrdType': '2',
        'ClOrdID': '*',
        'LastQty': venue_qty,
        'Text': text_f,
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '*',
        'OrdStatus': '2',
        'Price': 21,
        'Currency': currency,
        'TimeInForce': tif_ioc,
        'Instrument': '*',
        'ExecType': "F",
        'ExDestination': ex_destination_1,
        'LeavesQty': '0'
    }
    time.sleep(2)
    fix_verifier_bs.CheckExecutionReport(er_12, responce_new_order_single, direction='SECOND', case=case_id_5,  message_name='BS FIXBUYTH2 sent 35=8 Filled Paris', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus', 'TimeInForce'])
    
    # Check SS (FIXSELLQUOD5 35=8 on Filled Order)
    # er_13= {
    #     'Text': text_f,
    #     'TimeInForce': 0,
    #     'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
    #     'CumQty': qty,
    #     'ExecType': 'F',
    #     'OrdStatus': 2

    # }
    # fix_verifier_ss.CheckExecutionReport(er_13, responce_new_order_single, case=case_id_5, message_name='SS FIXSELLQUOD5 send 35=8 Filled', key_parameters=['OrdStatus', 'ExecType', 'ClOrdID', 'TimeInForce', 'Text']) 
    #endregion

    time.sleep(1)
    rule_destroyer(rule_list)
