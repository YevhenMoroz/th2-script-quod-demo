import os
import logging
import time
import math
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, NoMDEntries
from th2_grpc_common.common_pb2 import ConnectionID
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#text
text_pn = 'Pending New status'
text_n = 'New status'
text_c = 'order canceled'
text_f = 'Fill'
text_r = 'order replaced'

#algo param
percentage = 10
aggressivity = 1

#order param
qty = 500
max_would_shares_qty = 490
child_ioc_qty = 465
open_qty_after_ioc = qty - child_ioc_qty                        #35
last_would_child = max_would_shares_qty - child_ioc_qty         #25
last_open_order_qty = qty - max_would_shares_qty                #10
ltq = 200
mkd = 100
price_20 = 20
price = 19.995
price_23 = 23      
price_25 = 25
price_30 = 30   
child_ltq_qty = 23                  #round (ltq * percentage / (100 - percentage))   
child_mkd_qty = 12                  #round (mkd * percentage / (100 - percentage))   
side = 1
tif_day = 0
tif_ioc = 3
order_type = 2
currency = 'EUR'

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '1015'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-316-ganymede"
connectivity_fh = 'fix-feed-handler-316-ganymede'

instrument = {
            'Symbol': 'FR0010263202_EUR',
            'SecurityID': 'FR0010263202',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

trigger = {
            'TriggerType': 4,
            'TriggerPrice': 23
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_ioc_md_rule = rule_manager.add_NewOrdSingle_IOC_MarketData(connectivity_buy_side, account, ex_destination_1, price_23, child_ioc_qty, True, connectivity_fh, s_par, price_23, child_ioc_qty, [NoMDEntries(MDEntryType="0", MDEntryPx='20', MDEntrySize='100', MDEntryPositionNo="1"), NoMDEntries(MDEntryType="1", MDEntryPx='23', MDEntrySize='35', MDEntryPositionNo="1")], [NoMDEntries(MDUpdateAction='0', MDEntryType='2', MDEntryPx='25', MDEntrySize='200', MDEntryDate= datetime.utcnow().date().strftime("%Y%m%d"), MDEntryTime=datetime.utcnow().time().strftime("%H:%M:%S"))])

    nos_ioc_md_rule_1 = rule_manager.add_NewOrdSingle_IOC_MarketData(connectivity_buy_side, account, ex_destination_1, price_23, last_would_child, True, connectivity_fh, s_par, price_23, last_would_child, [NoMDEntries(MDEntryType="0", MDEntryPx='20', MDEntrySize='100', MDEntryPositionNo="1"), NoMDEntries(MDEntryType="1", MDEntryPx='23', MDEntrySize='10', MDEntryPositionNo="1")], [NoMDEntries(MDUpdateAction='0', MDEntryType='2', MDEntryPx='25', MDEntrySize='200', MDEntryDate= datetime.utcnow().date().strftime("%Y%m%d"), MDEntryTime=datetime.utcnow().time().strftime("%H:%M:%S"))])


    nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_20)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_ioc_md_rule, nos_ioc_md_rule_1, nos_rule1, nos_rule2, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def send_market_data(symbol: str, case_id :str, market_data ):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_fh)
    ))

def send_market_dataT(symbol: str, case_id :str, market_data ):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntriesIR': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataIncrementalRefresh', md_params, connectivity_fh)
    ))


def execute(report_id):
    try:
        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager_316 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': price_20,
                'MDEntrySize': mkd,
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': price_30,
                'MDEntrySize': mkd,
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data1) 

        market_data2 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': price_25,
                'MDEntrySize': ltq,
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
        send_market_dataT(s_par, case_id_0, market_data2)

        time.sleep(1)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        new_order_single_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif_day,
            'OrdType': order_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Price': price_25,
            'Currency': currency,
            'TargetStrategy': 2,
            'ExDestination': ex_destination_1,
            'TriggeringInstruction': trigger,
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'PercentageVolume',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': percentage
                },
                {
                    'StrategyParameterName': 'Aggressivity',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': aggressivity
                },
                {
                    'StrategyParameterName': 'MaxWouldPercentage',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '98'
                },
                {
                    'StrategyParameterName': 'WouldPriceReference',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'MAN'
                },
                {
                    'StrategyParameterName': 'WouldPriceOffset',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '0'
                }
            ]
        }

        fix_message_new_order_single = FixMessage(new_order_single_params)
        fix_message_new_order_single.add_random_ClOrdID()
        responce_new_order_single = fix_manager_316.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)
        
        time.sleep(1)

        nos_1 = dict(
            fix_message_new_order_single.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL5 receive 35=D')

        #Check that FIXQUODSELL6 sent 35=8 pending new
        er_1 ={
            'Account': client,
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
            'TimeInForce': tif_day,
            'ExecType': "A",
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty': qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(), 
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'Price': price_25,
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
            SettlType = '*',
            ExecRestatementReason='*',
            TriggeringInstruction = trigger
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        time.sleep(2)

        #region Child LTQ
        case_id_3 = bca.create_event("Check Child LTQ and MKD", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D Child LTQ)
        new_slice_1 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': child_ltq_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(new_slice_1, responce_new_order_single, case=case_id_3, message_name='BS FIXBUYTH2 sent 35=D New order Child LTQ', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': child_ltq_qty,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': child_ltq_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_3, message_name='FIXQUODSELL5 sent 35=8 Pending New Child LTQ', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='FIXQUODSELL5 sent 35=8 Child LTQ', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])
        #endregion

        # Check bs (FIXQUODSELL5 sent 35=D Child MKD)
        new_slice_2 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': child_mkd_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price_20,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(new_slice_2, responce_new_order_single, case=case_id_3, message_name='BS FIXBUYTH2 sent 35=D New order Child MKD', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])
        # Check that FIXBUYQUOD5 sent 35=8 pending new 
        er_6 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': child_mkd_qty,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price_20,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': child_mkd_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_6, responce_new_order_single, direction='SECOND', case=case_id_3, message_name='FIXQUODSELL5 sent 35=8 Pending New Child MKD', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_7 = dict(
            er_6,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_7, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='FIXQUODSELL5 sent 35=8 New MKD', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus'])
        #endregion

        time.sleep(1)

        #region WouldPrice childs and MKD
        case_id_5 = bca.create_event("Check WouldPrice childs and MKD", case_id)
        # Check bs (FIXBUYTH2 sent 35=8 on 35=F Child LTQ)
        er_8 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': child_ltq_qty,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*'
        }

        fix_verifier_bs.CheckExecutionReport(er_8, responce_new_order_single, direction='SECOND', case=case_id_5, message_name='BS FIXBUYTH2 sent 35=8 Cancel LTQ',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        
        #Check bs (FIXBUYTH2 sent 35=8 on 35=F Child MKD)
        er_9 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': child_mkd_qty,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*'
        }

        fix_verifier_bs.CheckExecutionReport(er_9, responce_new_order_single, direction='SECOND', case=case_id_5, message_name='BS FIXBUYTH2 sent 35=8 Cancel MKD',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        #endregion

        #region Would Price Child 465
        case_id_6 = bca.create_event("Check Would Price Child 465", case_id)
        #Check IOC order
        # Check bs (FIXQUODSELL5 sent 35=D Would Price Child 465)
        ioc_order_1 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': child_ioc_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price_23,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(ioc_order_1, responce_new_order_single, case=case_id_6, message_name='BS FIXBUYTH2 sent 35=D New order Would Price Child 465', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_10 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': child_ioc_qty,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price_23,
            'TimeInForce': tif_ioc,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': child_ioc_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_10, responce_new_order_single, direction='SECOND', case=case_id_6, message_name='FIXQUODSELL5 sent 35=8 Pending New Would Price Child 465', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_11 = dict(
            er_10,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_11, responce_new_order_single, direction='SECOND', case=case_id_6,  message_name='FIXQUODSELL5 sent 35=8 Would Price Child 465', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYTH2 sent 35=8 Fill
        er_12 = {
            'Account': account,
            'CumQty': child_ioc_qty,
            'LastPx': price_23,
            'ExecID': '*',
            'OrderQty': child_ioc_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'LastQty': child_ioc_qty,
            'Text': text_f,
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            'OrdStatus': '2',
            'Price': price_23,
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'ExecType': "F",
            'ExDestination': ex_destination_1,
            'LeavesQty': '0'
        }
        fix_verifier_bs.CheckExecutionReport(er_12, responce_new_order_single, direction='SECOND', case=case_id_6, message_name='BS FIXBUYTH2 sent 35=8 Fill Would Price Child 465',key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'TimeInForce', 'Price'])
        #endregion
        time.sleep(1)
        #region Would Price Child 25
        case_id_7 = bca.create_event("Check Would Price Child 25", case_id)
        #Check IOC order
        # Check bs (FIXQUODSELL5 sent 35=D Would Price Child 25)
        ioc_order_2 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': last_would_child,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price_23,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(ioc_order_2, responce_new_order_single, case=case_id_7, message_name='BS FIXBUYTH2 sent 35=D New order Would Price Child 25', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_13 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': last_would_child,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price_23,
            'TimeInForce': tif_ioc,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': last_would_child
        }

        fix_verifier_bs.CheckExecutionReport(er_13, responce_new_order_single, direction='SECOND', case=case_id_7, message_name='FIXQUODSELL5 sent 35=8 Pending New Would Price Child 25', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_14 = dict(
            er_13,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_14, responce_new_order_single, direction='SECOND', case=case_id_7,  message_name='FIXQUODSELL5 sent 35=8 Would Price Child 465', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYTH2 sent 35=8 Fill
        er_15 = {
            'Account': account,
            'CumQty': last_would_child,
            'LastPx': price_23,
            'ExecID': '*',
            'OrderQty': last_would_child,
            'OrdType': order_type,
            'ClOrdID': '*',
            'LastQty': last_would_child,
            'Text': text_f,
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            'OrdStatus': '2',
            'Price': price_23,
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'ExecType': "F",
            'ExDestination': ex_destination_1,
            'LeavesQty': '0'
        }
        fix_verifier_bs.CheckExecutionReport(er_15, responce_new_order_single, direction='SECOND', case=case_id_7, message_name='BS FIXBUYTH2 sent 35=8 Fill Would Price Child 25',key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'TimeInForce', 'Price'])
        #endregion


        #region MKD 10
        case_id_8 = bca.create_event("Check MKD 10", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D Child MKD)
        new_slice_3 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': last_open_order_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price_20,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(new_slice_3, responce_new_order_single, case=case_id_8, message_name='BS FIXBUYTH2 sent 35=D New order Child MKD', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])
        # Check that FIXBUYQUOD5 sent 35=8 pending new 
        er_16 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': last_open_order_qty,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price_20,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': last_open_order_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_16, responce_new_order_single, direction='SECOND', case=case_id_8, message_name='FIXQUODSELL5 sent 35=8 Pending New Child MKD', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_17 = dict(
            er_16,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_17, responce_new_order_single, direction='SECOND', case=case_id_8,  message_name='FIXQUODSELL5 sent 35=8 New MKD', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus'])
        #endregion

        time.sleep(2)

        #region Cancel Algo Order
        case_id_9 = bca.create_event("Cancel Algo Order", case_id)
        # Cancel Order
        cancel_parms = {
        "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
        "Account": fix_message_new_order_single.get_parameter('Account'),
        "Side": fix_message_new_order_single.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
        }
    
        fix_cancel = FixMessage(cancel_parms)
        responce_cancel = fix_manager_316.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_9)
        
        time.sleep(1)

        # Check SS sent 35=F
        cancel_ss_param = {
            'Side': side,
            'Account': client,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'TransactTime': '*',
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }
        fix_verifier_ss.CheckOrderCancelRequest(cancel_ss_param, responce_cancel, direction='SECOND', case=case_id_9, message_name='SS FIXSELLQUOD5 sent 35=F Cancel',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        # Check bs (FIXBUYTH2 sent 35=8 on 35=F Child MKD)
        er_18 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': last_open_order_qty,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*'
        }

        fix_verifier_bs.CheckExecutionReport(er_18, responce_new_order_single, direction='SECOND', case=case_id_9, message_name='BS FIXBUYTH2 sent 35=8 Cancel LTQ',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        time.sleep(1)

        # Check ss (on FIXQUODSELL5 sent 35=8 on cancel)
        er_19 = {
        'ExecID': '*',
        'OrderQty': qty,
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '*',
        "OrdStatus": "4",
        'SettlDate': '*',
        'Currency': currency,
        'TimeInForce': tif_day,
        'ExecType': '4',
        'HandlInst': new_order_single_params['HandlInst'],
        'CxlQty': '*',
        'LeavesQty': '0',
        'NoParty': '*',
        'CumQty': max_would_shares_qty,
        'LastPx': '0',
        'OrdType': order_type,
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'TriggeringInstruction': trigger,
        'Price': price_25,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument,
        'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }

        fix_verifier_ss.CheckExecutionReport(er_19, responce_cancel, case=case_id_9, message_name='SS FIXSELLQUOD5 sent 35=8 Cancel', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])
        #endregion  
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_destroyer(rule_list)

