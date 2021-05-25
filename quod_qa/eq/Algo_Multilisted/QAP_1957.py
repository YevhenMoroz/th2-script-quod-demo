import os
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager


def execute(report_id):
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-310-columbia", "TRQX_CLIENT2", "TRQX", 20)
    ocr_rule = rule_manager.add_OCR("fix-bs-310-columbia")

    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager_qtwquod5 = FixManager('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-310-columbia', case_id)

    # Send NewOrderSingle
    multilisting_params = {
        'Account': "CLIENT2",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "1300",
        'TimeInForce': "1",
        'Price': "20",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'FR0010542647_EUR',
            'SecurityID': 'FR0010542647',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1008",
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
        ],
        "DisplayInstruction":
            {
                "DisplayQty": '1000'
            }
    }

    fix_message_multilisting = FixMessage(multilisting_params)
    fix_message_multilisting.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_multilisting)

    #Check on ss
    er_params_new ={
        'ExecID': '*',
        'OrderQty': multilisting_params['OrderQty'],
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': multilisting_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'ExecType': "0",
        'HandlInst': multilisting_params['HandlInst'],
        'LeavesQty': multilisting_params['OrderQty'],
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(), 
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '0',
        'Price': multilisting_params['Price'],
        'TargetStrategy': multilisting_params['TargetStrategy'],
        'Instrument': multilisting_params['Instrument']
    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce)
    #Check on bs
    new_order_single_bs = {
        'NoParty': '*',
        'Account': multilisting_params['Account'],        
        'OrderQty': multilisting_params['OrderQty'],
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'TransactTime': '*',
        'ChildOrderID': '*',
        'Side': multilisting_params['Side'],
        'Price': multilisting_params['Price'],
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'Instrument': '*',
        'HandlInst': '1',
        'ExDestination': multilisting_params['Instrument']['SecurityExchange']
    }
    fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce)

    #Check answer from sim
    er_bs_params = {
        'OrdStatus': "0",
        'Text': 'New status'
    }
    fix_verifier_bs.CheckExecutionReport(er_bs_params, responce, message_name="Check Sim's ExecutionReport",direction="SECOND")


    #Cancel order
    cancel_parms = {
        "ClOrdID": fix_message_multilisting.get_ClOrdID(),
        "Account": fix_message_multilisting.get_parameter('Account'),
        "Side": fix_message_multilisting.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_multilisting.get_ClOrdID()
    }
    fix_cancel = FixMessage(cancel_parms)
    responce_cancel = fix_manager_qtwquod5.Send_OrderCancelRequest_FixMessage(fix_cancel)
    cancel_er_params = {
        'ExecID': '*',
        'OrderQty': multilisting_params['OrderQty'],
        'NoStrategyParameters': '*',
        'LastQty': multilisting_params['OrderQty'],
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': multilisting_params['Side'],
        'AvgPx': '0',
        "OrdStatus": "4",
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'ExecType': '4',
        'HandlInst': multilisting_params['HandlInst'],
        'LeavesQty': '0',
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': multilisting_params['Price'],
        'TargetStrategy': multilisting_params['TargetStrategy'],
        'Instrument': multilisting_params['Instrument'],
        'OrigClOrdID': fix_message_multilisting.get_ClOrdID()
    }
    fix_verifier_ss.CheckExecutionReport(cancel_er_params, responce_cancel)

    time.sleep(1)
    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
