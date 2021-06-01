import os
import logging
import time
from datetime import datetime, timedelta
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

qty = 3000
text_pn='Pending New status'
text_n='New status'
text_ocrr='OCRRRule'
text_c='order canceled'
text_f='Fill'
text_ret = 'reached end time'
text_s = 'sim work'
text_r = 'order replaced'
side = 1
price = 1
tif_day = 0
tif_ioc = 3
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '1015'

now = datetime.today() - timedelta(hours=3)

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'

instrument = {
            'Symbol': 'FR0010263202_EUR',
            'SecurityID': 'FR0010263202',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    ocrr_rule = rule_manager.add_OrderCancelReplace_ExecutionReport(connectivity_buy_side)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_rule, ocrr_rule, ocr_rule]


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


def execute(report_id):
    try:
        rule_list = rule_creation();
        case_id = bca.create_event(os.path.basename(__file__), report_id)
        # Send_MarkerData
        fix_manager_310 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
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
        send_market_data(s_par, case_id_0, market_data1)  

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
            'Price': price,
            'Currency': currency,
            'TargetStrategy': 1005,
                    'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'StartDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'EndDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': (now + timedelta(minutes=3)).strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'Waves',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '3'
                },
                {
                    'StrategyParameterName': 'Aggressivity',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '1'
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
            SettlType='*'
        )
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        #region Slice 1
        case_id_2 = bca.create_event("Check Slice 1", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D Slice 1)
        new_slice_1 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': int(qty / 3),
            'OrdType': order_type,
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
        fix_verifier_bs.CheckNewOrderSingle(new_slice_1, responce_new_order_single, case=case_id_2, message_name='BS FIXBUYTH2 sent 35=D New order Slice 1', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(qty / 3),
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

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 Pending New Slice 1', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
            OrderQty=int(qty / 3),
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='FIXQUODSELL5 sent 35=8 New Slice 1', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        
        time.sleep(70)

        # Check BS (FIXBUYTH2 35=8 on 35=G)
        replace_param_slice1 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(qty / 3),
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_r,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '0',
            'Price': price,
            'TimeInForce': tif_ioc,
            'ExecType': '5',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }
        fix_verifier_bs.CheckExecutionReport(replace_param_slice1, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='BS FIXSELLQUOD5 sent 35=8 Replace Slice 1',key_parameters=['Text', 'TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])
        
        # Check BS (FIXBUYTH2 send 35=8 on Cancel)
        cancel_r_param1 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': int(qty / 3),
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'OrderID': '*',
            'TransactTime': '*',
            'ChildOrderID': '*',
            'Side': side,
            'Price': price,
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange'],
            'OrigClOrdID': '*'
        }
        fix_verifier_bs.CheckOrderCancelReplaceRequest(cancel_r_param1, responce_new_order_single, case=case_id_2, message_name='FIXBUYTH2 sent 35=8 Cancel Slice 1', key_parameters=['Text', 'TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])


        # Check BS (FIXBUYTH2 35=8 on 35=G)
        er_4 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(qty / 3),
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'Price': price,
            'TimeInForce': tif_ioc,
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='BS FIXBUYTH2 sent 35=8 Cancel Slice 1',key_parameters=['TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])
        #endregion

        #region Slice 2
        case_id_3 = bca.create_event("Create Slice 2", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D Slice 2)
        new_slice_2 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': int(qty / 3 * 2),
            'OrdType': order_type,
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
        fix_verifier_bs.CheckNewOrderSingle(new_slice_2, responce_new_order_single, case=case_id_3, message_name='BS FIXBUYTH2 sent 35=D New order Slice 2', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])
        # Check that FIXBUYQUOD5 sent 35=8 pending new 
        er_5 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(qty / 3 * 2),
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

        fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_3, message_name='FIXQUODSELL5 sent 35=8 Pending New Slice 2', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_6 = dict(
            er_5,
            OrdStatus='0',
            ExecType="0",
            OrderQty=int(qty / 3 * 2),
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_6, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='FIXQUODSELL5 sent 35=8 New Slice 3', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus'])
        
        time.sleep(75)
        # Check BS (FIXBUYTH2 35=8 on 35=G)
        replace_param_slice2 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(qty / 3 * 2),
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_r,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '0',
            'Price': price,
            'TimeInForce': tif_ioc,
            'ExecType': '5',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }
        fix_verifier_bs.CheckExecutionReport(replace_param_slice2, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='BS FIXSELLQUOD5 sent 35=8 Replace Slice 2',key_parameters=['Text', 'TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])
        
        # Check BS (FIXBUYTH2 send 35=8 on Cancel)
        cancel_r_param2 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': int(qty / 3 * 2),
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'OrderID': '*',
            'TransactTime': '*',
            'ChildOrderID': '*',
            'Side': side,
            'Price': price,
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange'],
            'OrigClOrdID': '*'
        }
        fix_verifier_bs.CheckOrderCancelReplaceRequest(cancel_r_param2, responce_new_order_single, case=case_id_3, message_name='FIXBUYTH2 sent 35=8 Cancel Slice 2', key_parameters=['Text', 'TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])


        # Check BS (FIXBUYTH2 35=8 on 35=G)
        er_7 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(qty / 3 * 2),
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'Price': price,
            'TimeInForce': tif_ioc,
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }
        fix_verifier_bs.CheckExecutionReport(er_7, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='BS FIXBUYTH2 sent 35=8 Cancel Slice 2',key_parameters=['TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])
        #endregion
        
        #region Slice 3
        case_id_4 = bca.create_event("Create Slice 3", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D Slice 3)
        new_slice_3 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': qty,
            'OrdType': order_type,
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
        fix_verifier_bs.CheckNewOrderSingle(new_slice_3, responce_new_order_single, case=case_id_4, message_name='BS FIXBUYTH2 sent 35=D New order Slice 3', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])
        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_8 = {
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

        fix_verifier_bs.CheckExecutionReport(er_8, responce_new_order_single, direction='SECOND', case=case_id_4, message_name='FIXQUODSELL5 sent 35=8 Pending New Slice 3', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_9 = dict(
            er_8,
            OrdStatus='0',
            ExecType="0",
            OrderQty=qty,
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_9, responce_new_order_single, direction='SECOND', case=case_id_4,  message_name='FIXQUODSELL5 sent 35=8 New Slice 3', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        
        time.sleep(80)
        # Check BS (FIXBUYTH2 35=8 on 35=G)
        replace_param_slice3 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_r,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '0',
            'Price': price,
            'TimeInForce': tif_ioc,
            'ExecType': '5',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }
        fix_verifier_bs.CheckExecutionReport(replace_param_slice3, responce_new_order_single, direction='SECOND', case=case_id_4,  message_name='BS FIXSELLQUOD5 sent 35=8 Replace Slice 3',key_parameters=['Text', 'TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])
        
        # Check BS (FIXBUYTH2 send 35=8 on Cancel)
        cancel_r_param3 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'OrderID': '*',
            'TransactTime': '*',
            'ChildOrderID': '*',
            'Side': side,
            'Price': price,
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange'],
            'OrigClOrdID': '*'
        }
        fix_verifier_bs.CheckOrderCancelReplaceRequest(cancel_r_param3, responce_new_order_single, case=case_id_4, message_name='FIXBUYTH2 sent 35=8 Cancel Slice 3', key_parameters=['Text', 'TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])


        # Check BS (FIXBUYTH2 35=8 on 35=G)
        er_10 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'Price': price,
            'TimeInForce': tif_ioc,
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }
        fix_verifier_bs.CheckExecutionReport(er_10, responce_new_order_single, direction='SECOND', case=case_id_4,  message_name='BS FIXBUYTH2 sent 35=8 Cancel Slice 3',key_parameters=['TimeInForce', 'OrderQty', 'Price', 'OrdStatus', 'ExecType'])
        #endregion

        #region Cancel Algo Order
        case_id_6 = bca.create_event("Cansel Algo Order", case_id)
        # Check SS (on FIXQUODSELL5 sent 35=8 Cancel)
        cancel_param = {
        'ExecID': '*',
        'OrderQty': qty,
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        "OrdStatus": "4",
        'SettlDate': '*',
        'Currency': currency,
        'TimeInForce': tif_day,
        'ExecType': '4',
        'HandlInst': new_order_single_params['HandlInst'],
        'LeavesQty': '0',
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': order_type,
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'LastMkt': ex_destination_1,
        'Text': text_ret,
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': price,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument,
        }

        fix_verifier_ss.CheckExecutionReport(cancel_param, responce_new_order_single, case=case_id_6, message_name='SS FIXSELLQUOD5 sent 35=8 Cancel', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])
        #endregion
    
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)