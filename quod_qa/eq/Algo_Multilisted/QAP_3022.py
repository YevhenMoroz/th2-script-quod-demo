import os
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

    nos_rule = rule_manager.add_NOS("fix-bs-310-columbia", "XPAR_CLIENT2")

    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager_qtwquod5 = FixManager('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-310-columbia', case_id)

    # Send NewOrderSingle
    multilisting_params = {
        'Account': "CLIENT2",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "1000",
        'TimeInForce': "4",
        'Price': "35",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'FR0000125007_EUR',
            'SecurityID': 'FR0000125007',
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
            },
            {
                'StrategyParameterName': 'AllowedPassiveVenues',
                'StrategyParameterType': '14',
                'StrategyParameterValue': 'PARIS'
            }
        ]
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

    er_params_new ={
        'ExecID': '*',
        'OrderQty': multilisting_params['OrderQty'],
        'NoStrategyParameters': '*',
        'LastQty': '0',
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': multilisting_params['Side'],
        'AvgPx': '0',
        "OrdStatus": "4",
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'ExecType': "4",
        'HandlInst': multilisting_params['HandlInst'],
        'LeavesQty': '0',
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'Text': 'no liquidity found',
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '*',
        'Price': multilisting_params['Price'],
        'TargetStrategy': multilisting_params['TargetStrategy'],
        'Instrument': multilisting_params['Instrument']
    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce)

    rule_manager.remove_rule(nos_rule)
