import logging
import os
import time
from datetime import datetime
from copy import deepcopy
from datetime import datetime
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
display_qty = 1000
dec_qty = 900
price = 20
side = 1
text_pn='Pending New status'
text_n='New status'
text_c='order canceled'
currency = 'EUR'
ex_destination_1 = "XPAR"
ex_destination_2 = "TRQX"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
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
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_2, price)
    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_rule, ocrr_rule, ocr_rule]

def rule_destroyer(list_rules):
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
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        rule_list = rule_creation()

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

        case_id_1 = bca.create_event("Create Algo Order", case_id)
        # Send NewOrderSingle
        new_order_single_params = {
            'Account': client,
            'HandlInst': "2",
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': "0",
            'Price': "20",
            'OrdType': "2",
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': 1004,
            "ExDestination": ex_destination_1,
            "DisplayInstruction":{
                    'DisplayQty' : display_qty
                },

        }
        fix_message_new_order_single = FixMessage(new_order_single_params)
        fix_message_new_order_single.add_random_ClOrdID()
        responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)

        #Check on ss
        er_params_pending ={
            'ExecType': "A",
            'OrdStatus': 'A',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        }
        fix_verifier_ss.CheckExecutionReport(er_params_pending, responce_new_order_single)
        
        #Check on ss
        er_params_new ={
            'ExecType': "0",
            'OrdStatus': '0',
            'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        }
        fix_verifier_ss.CheckExecutionReport(er_params_new, responce_new_order_single)
        
        #Check on bs
        fix_message_new_order_single_bs = {
            'OrderQty': new_order_single_params['DisplayInstruction']['DisplayQty'],
            'Side': new_order_single_params['Side'],
            'Price': new_order_single_params['Price']
        }
        fix_verifier_bs.CheckNewOrderSingle(fix_message_new_order_single_bs, responce_new_order_single)

        #region Modify order
        case_id_3 = bca.create_event("Modify Order", case_id)
        # Send OrderCancelReplaceRequest  
        fix_modify_message = deepcopy(fix_message_new_order_single)
        fix_modify_message.change_parameters({'ExDestination': ex_destination_2})
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_3)
        #endregion

        time.sleep(1)
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

        time.sleep(1)

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
        er_9 = {
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

        fix_verifier_bs.CheckExecutionReport(er_9, responce_cancel, direction='SECOND', case=case_id_4, message_name='BS FIXBUYTH2 sent 35=8 Cancel',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        er_10 = {
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
            'TimeInForce': new_order_single_params['TimeInForce'],
            'ExecType': '4',
            'HandlInst': new_order_single_params['HandlInst'],
            'LeavesQty': '0',
            'NoParty': '*',
            'MaxFloor': dec_qty,
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': new_order_single_params['OrdType'],
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': new_order_single_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'Price': price,
            'TargetStrategy': new_order_single_params['TargetStrategy'],
            'Instrument': instrument,
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }
        fix_verifier_ss.CheckExecutionReport(er_10, responce_cancel, case=case_id_4, message_name="SS FIXSELLQUOD5 send 35=8 Cancel")
        #endregion

    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)
