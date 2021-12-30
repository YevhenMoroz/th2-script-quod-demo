import os
import logging
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#text
text_pn='Pending New status'
text_n='New status'
text_c='order canceled'

#order param
qty = 1300
tif_gtd = 6
stop_price = 30
side = 1
order_type_stop = 3
order_type_limit = 2
order_type_market = 1
currency = 'EUR'

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
s_par = '734'
s_trqx = '3416'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'
connectivity_fh = 'fix-fh-310-columbia'

instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nosm_rule = rule_manager.add_NewOrdSingle_Market(connectivity_buy_side, account, ex_destination_1, False, 0, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nosm_rule, ocr_rule]


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
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

        expire_date = (datetime.today() + timedelta(days=2)).strftime("%Y%m%d")

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
        send_market_data(s_trqx, case_id_0, market_data2)    
        

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        new_order_single_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif_gtd,
            'StopPx': stop_price,
            'OrdType': order_type_stop,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': currency,
            'ExpireDate': expire_date,
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
            'Account': client,
            'ExecID': '*',
            'OrderQty': qty,
            'ExpireDate': expire_date,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Currency': currency,
            'TimeInForce': tif_gtd,
            'ExecType': "A",
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty': qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type_stop,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(), 
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'StopPx': stop_price,
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
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        
        case_id_2 = bca.create_event("Send Market Data", case_id)

        # Send MarketData
        MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol="734",
            connection_id=ConnectionID(session_alias=connectivity_fh)
        )).MDRefID

        mdir_params_trade = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '35',
                    'MDEntrySize': '2000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', connectivity_fh, case_id_2,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, connectivity_fh)
        ))
        time.sleep(10)
        mdir_params_trade = {
            'MDReqID': MDRefID_1,
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '35',
                    'MDEntrySize': '2000',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', connectivity_fh, case_id_2,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, connectivity_fh)
        ))
        time.sleep(2)
        #endregion

        #region Check Buy Side
        case_id_3 = bca.create_event("Check Buy Side", case_id)
        # Check bs (FIXQUODSELL5 sent 35=D pending new)
        new_order_single_bs = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': qty,
            'ExpireDate': expire_date,
            'OrdType': order_type_market,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce_new_order_single, case=case_id_3, message_name='BS FIXBUYTH2 sent 35=D New order', key_parameters=['OrderQty', 'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': qty,
            'Text': text_pn,
            'OrdType': order_type_market,
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': qty
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_3, message_name='FIXQUODSELL5 sent 35=8 Pending New', key_parameters=['TimeInForce' ,'OrderQty', 'ExecType', 'OrdStatus'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
            OrderQty=qty,
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])
        #endregion


        time.sleep(3)
        #region Cancel order
        case_id_4 = bca.create_event("Cancel Order", case_id)
        # Check ExecutionReport FIXBUYTH2 35=8 on 35=F
        er_7 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': order_type_market,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'TimeInForce': tif_gtd,
            'ExecType': '4',
            'ExDestination': ex_destination_1,
            'LeavesQty': '0',
        }

        fix_verifier_bs.CheckExecutionReport(er_7, responce_new_order_single, direction='SECOND', case=case_id_4, message_name='BS FIXBUYTH2 sent 35=8 Cancel',key_parameters=['OrdType', 'Text', 'OrderQty', 'ExecType', 'OrdStatus'])

        # Check SS (FIXSELLQUOD5 35=8 on 35=F)
        er_8 = {
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrdStatus': '4',
            'ExecID': '*',
            'OrderQty': qty,
            'ExpireDate': expire_date,
            'LastQty': 0,
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': 0,
            'SettlDate': '*',
            'Currency': 'EUR',
            'TimeInForce': tif_gtd,
            'ExecType': 4,
            'HandlInst': 2,
            'LeavesQty': 0,
            'NoParty': '*',
            'CumQty': 0,
            'LastPx': 0,
            'OrdType': order_type_stop,
            'OrderCapacity': 'A',
            'QtyType': 0,
            'ExecRestatementReason': 4,
            'TargetStrategy': 1008,
            'Instrument': '*',
            'StopPx': stop_price,
            'NoStrategyParameters': '*',    
            'Text': '*',
            'LastMkt': ex_destination_1     
        }
        fix_verifier_ss.CheckExecutionReport(er_8, responce_new_order_single, case=case_id_4, message_name="SS FIXSELLQUOD5 send 35=8 Cancel", key_parameters=['OrdStatus', 'ExecType', 'TimeInForce', 'OrdType', 'OrderID', 'ExpireDate'])
        #endregion

        time.sleep(1)
    except:
        logging.error("Error execution",exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=report_id)
    finally:
        rule_destroyer(rule_list)