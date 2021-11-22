import logging
import os
import time
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca

from test_cases.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_cases.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT2")
    ocr_rule = rule_manager.add_OCR("fix-bs-eq-paris")
    ocrr_rule = rule_manager.add_OCRR("fix-bs-eq-paris")

    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
    fix_verifier_ss = FixVerifier('gtwquod5', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-eq-paris', case_id)

    # Send NewOrderSingle
    iceberg_params = {
        'Account': "CLIENT2",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "1000",
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
        'TargetStrategy': "1004",
        "DisplayInstruction":
            {
                "DisplayQty": '50'
            }

    }
    fix_message_iceberg = FixMessage(iceberg_params)
    fix_message_iceberg.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_iceberg)

    #Check on ss
    er_params_new ={
        'ExecType': "0",
        'OrdStatus': '0',
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,

    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce)
    #Check on bs
    new_order_single_bs = {
        'OrderQty': iceberg_params['DisplayInstruction']['DisplayQty'],
        'Side': iceberg_params['Side'],
        'Price': iceberg_params['Price']
    }
    fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce)


    # Send OrderCancelReplaceRequest
    fix_modify_message = deepcopy(fix_message_iceberg)
    fix_modify_message.change_parameter("DisplayInstruction",{"DisplayQty": '100'})

    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    amend_responce = fix_manager_qtwquod5.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)

    time.sleep(1)

    # Check on bs
    new_order_single_bs_modified = {
        'OrderQty': 100,
        'Side': iceberg_params['Side'],
        'OrigClOrdID': '*'
    }
    fix_verifier_bs.CheckOrderCancelReplaceRequest(new_order_single_bs_modified, responce)

    #Cancel order
    iceberg_cancel_parms = {
        "ClOrdID": fix_message_iceberg.get_ClOrdID(),
        "Account": fix_message_iceberg.get_parameter('Account'),
        "Side": fix_message_iceberg.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_iceberg.get_ClOrdID()
    }
    fix_cancel = FixMessage(iceberg_cancel_parms)
    responce_cancel = fix_manager_qtwquod5.Send_OrderCancelRequest_FixMessage(fix_cancel)
    cancel_er_params = {
        "OrdStatus": "4"
    }
    fix_verifier_ss.CheckExecutionReport(cancel_er_params,responce_cancel )
    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
    rule_manager.remove_rule(ocrr_rule)
