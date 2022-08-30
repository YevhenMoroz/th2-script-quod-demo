import os
import logging
import time
import math
from datetime import datetime, timedelta
from copy import deepcopy
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import NoMDEntries, RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

waves = 3
qty = 500
child_qty = 150
qty_4 = 167
child_day_qty = round(qty / waves)
would_price_qty = qty - child_qty  #350
text_pn = 'Pending New status'
text_n = 'New status'
text_ocrr = 'OCRRRule'
text_c = 'order canceled'
text_ret = 'reached end time'
text_r = 'order replaced'
side = 1
price = 20
price_2 = 19.995
tif_day = 0
tif_ioc = 3
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
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

def rule_creation():
    rule_manager = RuleManager()
    nos_ioc_md_rule = rule_manager.add_NewOrdSingle_IOC_MarketData(connectivity_buy_side, account, ex_destination_1, price_2, qty_4, False, connectivity_fh, s_par, price_2, would_price_qty, [NoMDEntries(MDEntryType="0", MDEntryPx="0", MDEntrySize="0", MDEntryPositionNo="1"), NoMDEntries(MDEntryType="1", MDEntryPx="20", MDEntrySize="500", MDEntryPositionNo="1")], [NoMDEntries(MDUpdateAction='0', MDEntryType='2', MDEntryPx='40', MDEntrySize='1000', MDEntryDate= datetime.utcnow().date().strftime("%Y%m%d"), MDEntryTime=datetime.utcnow().time().strftime("%H:%M:%S"))])

    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)

    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)

    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_ioc_md_rule, nos_rule, ocrr_rule, ocr_rule]


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
        now = datetime.today() - timedelta(hours=3)
        waves = 3

        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager_310 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': price_2,
                'MDEntrySize': would_price_qty,
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data1) 

        market_data2 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': price,
                'MDEntrySize': qty,
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
        send_market_dataT(s_par, case_id_0, market_data2)

        #time.sleep(1)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        new_order_single_params = {
            'Account': client,
            'ClOrdID': 'QAP_4876_' + bca.client_orderid(9),
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
            'ExDestination': ex_destination_1,
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
                    'StrategyParameterValue': waves
                },
                {
                    'StrategyParameterName': 'MaxWouldPercentage',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '70'
                },
                {
                    'StrategyParameterName': 'WouldPriceReference',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LTP'
                },
                {
                    'StrategyParameterName': 'WouldPriceOffset',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '-1'
                }
            ]
        }

        fix_message_new_order_single = FixMessage(new_order_single_params)
        responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)

        nos_1 = dict(
            fix_message_new_order_single.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL5 receive 35=D')

        #Check that FIXQUODSELL5 sent 35=8 pending new
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
            SettlType = '*',
            ExecRestatementReason='*',
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        #region Slice 1
        case_id_2 = bca.create_event("Check Slice 1", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D Slice 1)
        would_price_cild = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': would_price_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price_2,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_ioc,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(would_price_cild, responce_new_order_single, case=case_id_2, message_name='BS FIXBUYTH2 sent 35=D New order WouldPrice Child', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': would_price_qty,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price_2,
            'TimeInForce': tif_ioc,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': would_price_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 Pending New WouldPrice Pending', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='FIXQUODSELL5 sent 35=8 WouldPrice New', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        #Check would price order eliminated
        er_5 = {            
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': would_price_qty,
            'OrdType': '2',
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'TimeInForce': tif_ioc,
            'ExecType': '4',
            'ExDestination': ex_destination_1,
            'LeavesQty': '0'
        }
        fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='FIXQUODSELL5 sent 35=8 WouldPrice Eliminated', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Text'])

        #Check order for slice 1
        new_slice_1 = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': child_qty,
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
        fix_verifier_bs.CheckNewOrderSingle(new_slice_1, responce_new_order_single, case=case_id_2, message_name='BS FIXBUYTH2 sent 35=D New order Slice 1', key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_6 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': child_qty,
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
            'LeavesQty': child_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_6, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='FIXQUODSELL5 sent 35=8 Pending New Slice 1', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_7 = dict(
            er_6,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_7, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='FIXQUODSELL5 sent 35=8 Slice 1', key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price', 'TimeInForce'])

        time.sleep(2)

        #region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", case_id)
        # Cancel Order
        cancel_parms = {
        "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
        "Account": fix_message_new_order_single.get_parameter('Account'),
        "Side": fix_message_new_order_single.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
        }
    
        fix_cancel = FixMessage(cancel_parms)
        responce_cancel = fix_manager_310.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_4)

        # Check SS sent 35=F
        cancel_ss_param = {
            'Side': side,
            'Account': client,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'TransactTime': '*',
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }
        fix_verifier_ss.CheckOrderCancelRequest(cancel_ss_param, responce_cancel, direction='SECOND', case=case_id_4, message_name='SS FIXSELLQUOD5 sent 35=F Cancel',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        
        time.sleep(1)

        # Check ss (on FIXQUODSELL5 sent 35=8 on cancel)
        er_11 = {
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
            'CxlQty': qty,
            'LeavesQty': '0',
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'SettlType': '*',
            'Price': price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument,
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }

        fix_verifier_ss.CheckExecutionReport(er_11, responce_cancel, case=case_id_4, message_name='SS FIXSELLQUOD5 sent 35=8 Cancel', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])
        #endregion  

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_destroyer(rule_list)

