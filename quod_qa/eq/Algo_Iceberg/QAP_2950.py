import logging
import os
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 2000
display_qty = 100
limit = 20
side = 1
lookup = "FR0010542647_EUR"
security_id = "FR0010542647"
ex_destination_1 = "XPAR"
ex_destination_2 = "TRQX"
client = "CLIENT1"
order_type = "Limit"
case_name = os.path.basename(__file__)

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-" + ex_destination_1.lower(), ex_destination_1 + "_" + client, ex_destination_1, limit)
    # ocr_rule = rule_manager.add_OrderCancelRequest('fix-bs-eq-' + ex_destination_1.lower(), ex_destination_1 + '_' + client, ex_destination_1, True)
    # ocrr_rule = rule_manager.add_OCRR("fix-bs-eq-paris")
    # return [nos_rule, ocr_rule, ocrr_rule]
    return [nos_rule]

def rule_destroyer(list_rules):
    rule_manager = RuleManager()
    for rule in list_rules:
        rule_manager.remove_rule(rule)

def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    rule_list = rule_creation()
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
    fix_verifier_ss = FixVerifier('gtwquod5', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-eq-paris', case_id)

    # Send NewOrderSingle
    iceberg_params = {
        'Account': client,
        'HandlInst': "2",
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': "0",
        'Price': "20",
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': lookup,
            'SecurityID': lookup[:-4],
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1004",
        "ExDestination": ex_destination_1,
        "DisplayInstruction":
            {
                "DisplayQty": '50'
            }

    }
    fix_message_iceberg = FixMessage(iceberg_params)
    fix_message_iceberg.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_iceberg)

    # #Check on ss
    # er_params_pending ={
    #     'ExecType': "A",
    #     'OrdStatus': 'A',
    #     'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
    # }
    # fix_verifier_ss.CheckExecutionReport(er_params_pending, responce)
    #
    # #Check on ss
    # er_params_new ={
    #     'ExecType': "0",
    #     'OrdStatus': '0',
    #     'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
    # }
    # fix_verifier_ss.CheckExecutionReport(er_params_new, responce)
    #
    # #Check on bs
    # new_order_single_bs = {
    #     'OrderQty': iceberg_params['DisplayInstruction']['DisplayQty'],
    #     'Side': iceberg_params['Side'],
    #     'Price': iceberg_params['Price']
    # }
    # fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce)
    #
    # # Send OrderCancelReplaceRequest
    # fix_modify_message = deepcopy(fix_message_iceberg)
    # fix_modify_message.change_parameters({'ExDestination': ex_destination_2})
    # fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    # fix_manager_qtwquod5.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)

    rule_destroyer(rule_list)
