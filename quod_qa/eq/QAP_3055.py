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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):

    case_id = bca.create_event("Test", report_id)
    fix_manager_fh_trqx = FixManager('fix-fh-eq-trqx', case_id)
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)

    iceberg_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "200",
        'TimeInForce': "0",
        'Price': "10.6",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'IT0000076189_EUR',
            'SecurityID': 'IT0000076189',
            'SecurityIDSource': '4',
            'SecurityExchange': 'MTAA'
        },
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1004",
        "DisplayInstruction":
            {
                "DisplayQty": '50'
            }

    }
    fix_message_iceberg = FixMessage(iceberg_params)
    fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_iceberg)

    iceberg_modify_parms = deepcopy(iceberg_params)
