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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 1000
text_f='Fill'
text_pn='Pending New status'
text_n='New status'
text_ocrr='OCRRRule'
text_c='order canceled'
tif_ioc = 3
price = 40
lastpx = 40
side = 1
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = "Limit"
account = 'XPAR_CLIENT2'
currency = 'EUR'

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
    nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, qty, price)
    return [nos_ioc_rule]


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
    

    #region Send NewOrderSingle (35=D)
    case_id_1 = bca.create_event("Create Algo Order", case_id)
    new_order_single_params = {
        'Account': client,
        'HandlInst': 2,
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': tif_ioc,
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
    nos_ioc_1 = dict(
        fix_message_new_order_single.get_parameters(),
        TransactTime='*',
        ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

    fix_verifier_ss.CheckNewOrderSingle(nos_ioc_1, responce_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL5 receive 35=D')

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
        'TimeInForce': tif_ioc,
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
        'TimeInForce': tif_ioc,
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
        'TimeInForce': tif_ioc,
        'ExecType': "A",
        'ExDestination': ex_destination_1,
        'LeavesQty': qty
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

    er_5 = {
        'Account': account,
        'CumQty': qty,
        'LastPx': lastpx,
        'ExecID': '*',
        'OrderQty': qty,
        'OrdType': '2',
        'ClOrdID': '*',
        'LastQty': qty,
        'Text': text_f,
        'OrderCapacity': new_order_single_params['OrderCapacity'],
        'OrderID': '*',
        'TransactTime': '*',
        'Side': side,
        'AvgPx': '*',
        'OrdStatus': '2',
        'Price': price,
        'Currency': currency,
        'TimeInForce': tif_ioc,
        'Instrument': '*',
        'ExecType': "F",
        'ExDestination': ex_destination_1,
        'LeavesQty': '0'
    }
    time.sleep(10)
    fix_verifier_bs.CheckExecutionReport(er_5, responce_new_order_single, direction='SECOND', case=case_id_2,  message_name='BS FIXBUYTH2 sent 35=8 Filled', key_parameters=['OrderQty', 'Price', 'ExecType', 'OrdStatus', 'TimeInForce'])
    #endregion

    #region Filled Order
    case_id_3 = bca.create_event("Check Sell Side", case_id)
    # Check SS (FIXSELLQUOD5 35=8 on Filled Order)
    er_6 = {
        'OrdStatus': '2',
        'ExecType': 'F',
        'Price': price,
        'OrderQty': qty,
        'TimeInForce': tif_ioc,
        'Text': text_f
    }
    fix_verifier_ss.CheckExecutionReport(er_6, responce_new_order_single, case=case_id_3, message_name='SS FIXSELLQUOD5 send 35=8 Filled', key_parameters=['TimeInForce','ExecType'])
    #endregion

    time.sleep(1)
    rule_destroyer(rule_list)