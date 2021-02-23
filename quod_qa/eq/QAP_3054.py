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
    case_id = bca.create_event("QAP-3029", report_id)
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
    fix_verifier_ss = FixVerifier('gtwquod3', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-eq-trqx', case_id)

    # Send NewOrderSingle
    iceberg_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "1000",
        'TimeInForce': "0",
        'Price': "20",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'FR0000054421_EUR',
            'SecurityID': 'FR0000054421',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
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
    fix_message_iceberg.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_iceberg)
    fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_iceberg)

    #Check on ss
    er_params_new ={
        'ExecType': "0",
        'OrdStatus': '0'
    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce)
    #Check on bs
    new_order_single_bs = {
        'OrderQty': 50,
        'Side': 2
    }
    fix_verifier_bs.CheckExecutionReport(new_order_single_bs, responce)


    # Send OrderCancelReplaceRequest
    fix_modify_message = deepcopy(fix_message_iceberg)
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_modify_message)

    #Check on bs
    new_order_single_bs_modified = {
        'OrderQty': 100,
        'Side': 2
    }
    fix_verifier_bs.CheckExecutionReport(new_order_single_bs_modified, responce)

    #Cancel order
    iceberg_cancel_parms = {
        "ClOrdID": fix_message_iceberg.get_ClOrdID(),
        "Account": fix_message_iceberg.get_parameter('Account'),
        "Side": fix_message_iceberg.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_iceberg.get_ClOrdID()
    }
    fix_cancel = FixMessage(iceberg_cancel_parms)
    fix_manager_qtwquod5.Send_OrderCancelReplaceRequest_FixMessage(fix_cancel)
    cancel_er_params = {
        "OrdStatus": "4"
    }
    fix_verifier_ss.CheckExecutionReport(cancel_er_params)
