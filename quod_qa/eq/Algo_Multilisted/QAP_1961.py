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

qty = 1300
price = 20
side = 1
expire_date = (datetime.today() + timedelta(days=2)).strftime("%Y%m%d")
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
    ocrr_rule = rule_manager.add_OCRR(connectivity_buy_side)
    return [nos_rule, ocr_rule, ocrr_rule]


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
    

    # Send NewOrderSingle
    case_id_1 = bca.create_event("Algo order creation", case_id)
    new_order_single_params = {
        'Account': client,
        'HandlInst': 2,
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': 6,
        'Price': price,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
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
    responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single)

    #Check on ss (FIXQUODSELL5 receive 35=D)

    # Send OrderCancelReplaceRequest  
    fix_modify_message = deepcopy(fix_message_new_order_single)
    fix_modify_message.change_parameters({'TimeInForce': '0'})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_modify_message.remove_tag('ExprieDate')
    fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)

    time.sleep(2)

    
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


    time.sleep(1)
    rule_destroyer(rule_list)