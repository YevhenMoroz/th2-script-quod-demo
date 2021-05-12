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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 1300
display_qty = 1000
price = 20
side = 1
currency = 'EUR'
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = "Limit"
account = 'XPAR_CLIENT2'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"

instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_rule, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def execute(report_id):
    rule_list = rule_creation();
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    # Send_MarkerData
    fix_manager_310 = FixManager(connectivity_sell_side, case_id)
    fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
    fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
    

    # Send NewOrderSingle (35=D)
    case_id_1 = bca.create_event("Algo order creation", case_id)
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
        "DisplayInstruction":{
            'DisplayQty' : display_qty
        },
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
    responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single)

    #Check on ss (FIXQUODSELL5 receive 35=D)
    er_params_new ={
        'ExecID': '*',
        'OrderQty': qty,
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'MaxFloor' : display_qty,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '*',
        'Currency': currency,
        'TimeInForce': new_order_single_params['TimeInForce'],
        'ExecType': "0",
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
        'SettlType': '0',
        'Price': price,
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument

    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce_new_order_single,   message_name='SS FIXQUODSELL5 receive 35=D', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])


    # Check bs (FIXQUODSELL5 sent 35=8 pending new)
    new_order_single_bs = {
        'NoParty': '*',
        'Account': account,        
        'OrderQty': display_qty,
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
    fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce_new_order_single, message_name='BS FIXBUYTH2 sent 35=8 pending new')


    # Send OrderCancelReplaceRequest  
    fix_modify_message = deepcopy(fix_message_new_order_single)
    fix_modify_message.change_parameters({'DisplayInstruction': {'DisplayQty': '900'}})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)

    time.sleep(2)

    
    # Check ss replace order
    replace_ss_params = {
        'ExecID': '*',
        'OrderQty': '900',
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '0',
        'Currency': currency,
        'TimeInForce': '0',
        'ExecType': '5',
        'HandlInst': new_order_single_params['HandlInst'],
        'LeavesQty': fix_message_new_order_single.get_parameter('OrderQty'),
        'NoParty': '*',
        'MaxFloor': '900',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': new_order_single_params['OrdType'],
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': fix_message_new_order_single.get_parameter('Price'),
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument,
        'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
    }
    time.sleep(1)

    fix_verifier_ss.CheckExecutionReport(replace_ss_params, responce_new_order_single,
                                         message_name='SS FIXSELLQUOD5 sent 35=G',
                                         key_parameters=['OrderQty', 'Price'])

    
    replace_bs_params = {
        'ExecID': '*',
        'OrderQty': '900',
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '0',
        'Currency': currency,
        'TimeInForce': '0',
        'ExecType': '5',
        'HandlInst': new_order_single_params['HandlInst'],
        'LeavesQty': fix_message_new_order_single.get_parameter('OrderQty'),
        'NoParty': '*',
        'MaxFloor': '900',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': new_order_single_params['OrdType'],
        'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': fix_message_new_order_single.get_parameter('Price'),
        'TargetStrategy': new_order_single_params['TargetStrategy'],
        'Instrument': instrument,
        'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
    }
    time.sleep(1)

    fix_verifier_bs.CheckNewOrderSingle(replace_bs_params, responce_new_order_single,
                                         message_name='BS FIXBUYTH2 sent 35=8',
                                         key_parameters=['OrderQty', 'Price'])

    #Cansel order
    cancel_parms = {
        "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
        "Account": fix_message_new_order_single.get_parameter('Account'),
        "Side": fix_message_new_order_single.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
    }
    
    fix_cancel = FixMessage(cancel_parms)
    responce_cancel = fix_manager_310.Send_OrderCancelRequest_FixMessage(fix_cancel)
    cancel_er_params = {
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
        'MaxFloor': '900',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': new_order_single_params['OrdType'],
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
    fix_verifier_ss.CheckExecutionReport(cancel_er_params, responce_cancel, message_name="Check cancel ER to SS")


    time.sleep(1)
    rule_destroyer(rule_list)