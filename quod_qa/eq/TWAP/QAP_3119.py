import os
import time
from copy import deepcopy
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager


def execute(report_id):
    rule_manager = RuleManager()
    ocr_rule = rule_manager.add_OCR("fix-bs-eq-paris")
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris",'XPAR_CLIENT2', 'XPAR', 20)

    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
    fix_verifier_ss = FixVerifier('gtwquod5', case_id)

    # Send NewOrderSingle

    now =datetime.today() - timedelta(hours=2)


    twap_params = {
        'Account': "CLIENT2",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "1300",
        'TimeInForce': "0",
        'Price': "20",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'FR0010380626_EUR',
            'SecurityID': 'FR0010380626',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1005",
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'StartDate',
                'StrategyParameterType': '19',
                'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")
            },
            {
                'StrategyParameterName': 'EndDate',
                'StrategyParameterType': '19',
                'StrategyParameterValue': (now + timedelta(minutes=2)).strftime("%Y%m%d-%H:%M:%S")
            },
            {
                'StrategyParameterName': 'Aggressivity',
                'StrategyParameterType': '1',
                'StrategyParameterValue': '1'
            }
        ]
    }

    fix_message_twap = FixMessage(twap_params)
    fix_message_twap.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_twap)

    #Check on ss
    er_params_new ={
        'ExecType': "0",
        'OrdStatus': '0',
        'TimeInForce': twap_params['TimeInForce'],
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'NoStrategyParameters': twap_params['NoStrategyParameters']

    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce, message_name='Check ER to SS', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

    time.sleep(1)
    #Cancel order
    cancel_parms = {
        "ClOrdID": fix_message_twap.get_ClOrdID(),
        "Account": fix_message_twap.get_parameter('Account'),
        "Side": fix_message_twap.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_twap.get_ClOrdID()
    }
    fix_cancel = FixMessage(cancel_parms)
    responce_cancel = fix_manager_qtwquod5.Send_OrderCancelRequest_FixMessage(fix_cancel)
    cancel_er_params = {
        "ClOrdID": fix_message_twap.get_ClOrdID(),
        "OrdStatus": "4"
    }
    fix_verifier_ss.CheckExecutionReport(cancel_er_params, responce_cancel, message_name="Check cancel ER to SS")

    time.sleep(1)
    rule_manager.remove_rule(ocr_rule)
    rule_manager.remove_rule(nos_rule)

