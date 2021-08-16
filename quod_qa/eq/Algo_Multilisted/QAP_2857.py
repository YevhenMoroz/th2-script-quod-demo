import logging
import os
from datetime import datetime
from custom import basic_custom_actions as bca

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-310-columbia", "XPAR_CLIENT1")

    connectivity = 'fix-ss-310-columbia-standart'
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    fix_manager_qtwquod3 = FixManager(connectivity, case_id)
    verifier = FixVerifier(connectivity, case_id)

    multilisting_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "222",
        'TimeInForce': "0",
        'Price': "10",
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
        'SecurityExchange': 'TRERROR',
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'AllowedPassiveVenues',
                'StrategyParameterType': '14',
                'StrategyParameterValue': 'TRQX_er'
            },
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

    fix_message_multilisting = FixMessage(multilisting_params)
    fix_message_multilisting.add_random_ClOrdID()
    response = fix_manager_qtwquod3.Send_NewOrderSingle_FixMessage(fix_message_multilisting)

    reject_parameters = {
        'Instrument': {
            'Symbol': 'FR0000125007_EUR',
            'SecurityExchange': 'XPAR'
        },
        'OrdStatus': '8',
        'Text': "unknown venue `TRQX_er'",
        'ClOrdID': fix_message_multilisting.get_ClOrdID()
    }
    verifier.CheckExecutionReport(reject_parameters, response)
    rule_manager.remove_rule(nos_rule)

