import os
import logging
import time
import math
from datetime import datetime, timedelta
from types import CellType
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID, NoMDEntries
from th2_grpc_common.common_pb2 import ConnectionID
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager, Simulators
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 300
mkd = 100
child_qty = 167
child_2_qty = 116
child_3_qty = 117
price_20 = 20
price = 19.995
price_23 = 23      
price_25 = 25
price_30 = 30    
waves = 3
aggressivity = 1  
percentage = 10
text_pn = 'Pending New status'
text_n = 'New status'
text_ocrr = 'OCRRRule'
text_c = 'order canceled'
text_f = 'Fill'
text_ret = 'reached end time'
text_lpfp = 'could not determine Limit price from Primary'
text_r = 'order replaced'
side = 1
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
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

        now = datetime.today() - timedelta(hours=3)
        n_waves = waves

        # Send_MarkerData
        fix_manager_316 = FixManager(connectivity_sell_side, case_id)
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
                'MDEntryPx': price_20,
                'MDEntrySize': qty,
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
            'ClOrdID': 'QAP_4751_' + bca.client_orderid(9),
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
                    'StrategyParameterName': 'LimitPriceReference',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'PRM'
                },
                {
                    'StrategyParameterName': 'LimitPriceOffset',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '-2'
                }
            ]
        }

        fix_message_new_order_single = FixMessage(new_order_single_params)
        responce_new_order_single = fix_manager_316.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)

        time.sleep(2)

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
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, responce_new_order_single, case=case_id_1, message_name='FIXQUODSELL5 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        #region Eliminated Algo Order
        case_id_9 = bca.create_event("Cancel Algo Order", case_id)
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
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': order_type,
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'Text': text_lpfp,
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': price_25,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument,
        }

        fix_verifier_ss.CheckExecutionReport(er_19, responce_new_order_single, case=case_id_9, message_name='SS FIXSELLQUOD5 sent 35=8 Cancel', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID', 'Text'])
        #endregion  
    except:
        logging.error("Error execution", exc_info=True)