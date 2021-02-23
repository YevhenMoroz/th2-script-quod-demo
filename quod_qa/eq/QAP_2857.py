import logging
import time
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):

    case_id = bca.create_event("Test", report_id)
    fix_manager_qtwquod3 = FixManager('gtwquod3', case_id)
    verifier = FixVerifier('gtwquod3', case_id)

    NOS = Stubs.simulator.createQuodNOSRule(request=TemplateQuodNOSRule(
            connection_id=ConnectionID(session_alias='fix-bs-eq-paris'),
            Account="XPAR_CLIENT1"
        ))

    sor_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "222",
        'TimeInForce': "0",
        'Price': "10.6",
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
                'StrategyParameterName': 'AllowedVenues',
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

    fix_message_sor = FixMessage(sor_params)
    fix_message_sor.add_random_ClOrdID()
    response = fix_manager_qtwquod3.Send_NewOrderSingle_FixMessage(fix_message_sor)

    reject_parameters = {
        'Instrument': {
            'Symbol': 'IT0000076189_EUR',
            'SecurityID': 'IT0000076189',
            'SecurityIDSource': '4',
            'SecurityExchange': 'MTAA'
        },
        'OrdStatus': '8',
        'Text': "unknown venue `TRXQ'",
        'ClOrdID': fix_message_sor.get_ClOrdID()
    }
    verifier.CheckExecutionReport(reject_parameters, response)
    Stubs.core.removeRule(NOS)

