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

qty = 1300
dec_qty = 900
text_pn='Pending New status'
text_n='New status'
text_ocrr='OCRRRule'
text_c='order canceled'
text_f='Fill'
side = 1
price = 20
dec_price = 19
tif_day = 0
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '734'
s_trqx = '3416'

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
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,  ex_destination_1, price)
    nos1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,  ex_destination_1, dec_price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    ocrr_rule = rule_manager.add_OCRR(connectivity_buy_side)
    return [nos_rule, nos1_rule, ocrr_rule, ocr_rule]


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
        rule_list = rule_creation()
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
        # Send NewOrderSingle
        new_order_single_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': "0",
            'Price': price,
            'OrdType': order_type,
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

        fix_verifier_ss.CheckNewOrderSingle(nos_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='SS FIXQUODSELL5 receive 35=D')


        #Check that FIXQUODSELL5 sent 35=8 pending new
        er_1 ={
            'ExecID': '*',
            'OrderQty':qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '0',
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': "0",
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty':qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(), 
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'Price': price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_1, responce_new_order_single, case=case_id_1, message_name='SS FIXQUODSELL5 sent 35=8 Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

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
        #endregion

        #region Check Buy Side
        case_id_2 = bca.create_event("Check Buy Side", case_id)
        # Check bs (FIXBUYTH2 sent 35=D pending new)
        new_order_single_bs = {
            'NoParty': '*',
            'Account': account,        
            'OrderQty': qty,
            'OrdType': 2,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': price,
            'SettlDate': '*',
            'Price': price,
            'Currency': currency,
            'TimeInForce': tif_day,
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
            'TimeInForce': tif_day,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': qty
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce_new_order_single, direction='SECOND', case=case_id_2, message_name='BS FIXBUYTH2 sent 35=8 Pending New', key_parameters=['ExecType', 'OrdStatus'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0",
            OrderQty=qty,
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='BS FIXBUYTH2 sent 35=8 New', key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        #endregion


        #region Modify order
        case_id_3 = bca.create_event("Modify Order", case_id)
        # Send OrderCancelReplaceRequest  
        fix_modify_message = deepcopy(fix_message_new_order_single)
        fix_modify_message.change_parameters({'Price': dec_price, 'OrderQty': dec_qty})
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_3)

        time.sleep(1)

        # Check SS (FIXSELLQUOD5 35=G)
        replace_ss_param = {
            'Account': client,
            'OrderQty': dec_qty,
            'OrdType': new_order_single_params['OrdType'],
            'NoStrategyParameters': new_order_single_params['NoStrategyParameters'],
            'TransactTime': '*',
            'Side': side,
            'Currency': currency,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'Instrument': instrument,
            'HandlInst': new_order_single_params['HandlInst'],
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'Price': dec_price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID(),
        }
        fix_verifier_ss.CheckOrderCancelReplaceRequest(replace_ss_param, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='SS FIXSELLQUOD5 sent 35=G Replace',key_parameters=['TimeInForce', 'OrderQty', 'Price'])

        # Check ExecutionReport FIXBUYTH2 35=8 on 35=F
        er_5 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': qty,
            'ClOrdID': '*',
            'Text': text_c,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0',
            'OrigClOrdID': '*',
        }

        fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_3, message_name='BS FIXBUYTH2 sent 35=8 Cancel',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        # Check ss replace order 35=8 on 35=G
        er_6 = {
            'ExecID': '*',
            'OrderQty': dec_qty,
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
            'LeavesQty': dec_qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': new_order_single_params['OrdType'],
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'Price': dec_price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument,
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrdStatus': '0'
        }

        fix_verifier_ss.CheckExecutionReport(er_6, responce_new_order_single, case=case_id_3, message_name='SS FIXSELLQUOD5 sent 35=8 Replace',key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus'])

        # Check that FIXQUODBUYTH2 receive 35=D
        replace_bs_params = {
            'NoParty': '*',
            'Account': account,
            'OrderQty': dec_qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'TransactTime': '*',
            'Side': side,
            'Price': dec_price,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': ex_destination_1,
        }

        fix_verifier_bs.CheckNewOrderSingle(replace_bs_params, responce_new_order_single, case=case_id_3, message_name='BS FIXBUYTH2 sent 35=D', key_parameters=['OrderQty', 'Price'])

       
        # Check that FIXBUYQUOD5 sent 35=8 pending new
        er_7 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': dec_qty,
            'Text': text_pn,
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': dec_price,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': dec_qty
        }

        fix_verifier_bs.CheckExecutionReport(er_7, responce_new_order_single, direction='SECOND', case=case_id_3, message_name='BS FIXBUYTH2 sent 35=8 Pending New', key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_8 = dict(
            er_7,
            OrdStatus='0',
            ExecType="0",
            Text=text_n,
        )
        fix_verifier_bs.CheckExecutionReport(er_8, responce_new_order_single, direction='SECOND', case=case_id_3,  message_name='BS FIXBUYTH2 sent 35=8 New', key_parameters=['Text', 'Price', 'OrderQty', 'ExecType', 'OrdStatus'])

        # Check SS (FIXSELLQUOD5 35=8 on 35=G)
        er_9 = {
            'ExecID': '*',
            'OrderQty': dec_qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '0',
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': '5',
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty': dec_qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': new_order_single_params['OrdType'],
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'Price': dec_price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument,
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrdStatus': '0'
        }

        fix_verifier_ss.CheckExecutionReport(er_9, responce_new_order_single, case=case_id_3, message_name='SS FIXSELLQUOD5 sent 35=8 Replace',key_parameters=['TimeInForce', 'OrderQty', 'Price', 'ExecType', 'OrdStatus'])
        #endregion

        time.sleep(3)

        #region Cancel order
        case_id_4 = bca.create_event("Cancel Order", case_id)
        # Cancel order
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

        # Check ExecutionReport FIXBUYTH2 35=8 on 35=F
        er_10 = {
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': dec_qty,
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

        fix_verifier_bs.CheckExecutionReport(er_10, responce_cancel, direction='SECOND', case=case_id_4, message_name='BS FIXBUYTH2 sent 35=8 Cancel',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        # Check SS (FIXSELLQUOD5 35=8 on 35=F)
        er_11 = {
            'ExecID': '*',
            'OrderQty': dec_qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            "OrdStatus": "4",
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': '4',
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty': '0',
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'Price': dec_price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument,
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }
        fix_verifier_ss.CheckExecutionReport(er_11, responce_cancel, case=case_id_4, message_name="SS FIXSELLQUOD5 send 35=8 Cancel", key_parameters=['OrdStatus', 'ExecType', 'TimeInForce', 'OrdType'])
        #endregion

        time.sleep(1)
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)

