import logging
import os
import time
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT2")
    ocr_rule = rule_manager.add_OCR("fix-bs-eq-paris")





    case_id = bca.create_event(os.path.basename(__file__), report_id)

    fix_manager_fh_paris = FixManager('fix-fh-eq-paris', case_id)
    fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
    fix_verifier_ss = FixVerifier('gtwquod5', case_id)
    fix_verifier_bs = FixVerifier('fix-bs-eq-paris', case_id)


    symbol = '1042'





    mdir_params_trade = {
        'NoMDEntriesIR': [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '1',
                'MDEntrySize': '100',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    }

    fix_message_md = FixMessage(mdir_params_trade)
    fix_manager_fh_paris.Send_MarketDataIncrementalRefresh_FixMessage(fix_message_md, symbol)

    # Send NewOrderSingle
    iceberg_params = {
        'Account': "CLIENT2",
        'HandlInst': "2",
        'Side': "1",
        'OrderQty': "1000",
        'TimeInForce': "0",
        'Price': "35",
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
        'TargetStrategy': "2",
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'PercentageVolume',
                'StrategyParameterType': '6',
                'StrategyParameterValue': '30.0'
            },
            {
                'StrategyParameterName': 'Aggressivity',
                'StrategyParameterType': '1',
                'StrategyParameterValue': '1'
            }
        ]

    }

    fix_message_PerVolume = FixMessage(iceberg_params)
    fix_message_PerVolume.add_random_ClOrdID()
    responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_PerVolume)

    #Check on ss
    er_params_new ={
        'ExecType': "0",
        'OrdStatus': '0',
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,

    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, responce)
    time.sleep(1)
    #Check on bs
    new_order_single_bs = {
        'Side': iceberg_params['Side'],
        'Price': iceberg_params['Price'],
        'TimeInForce': iceberg_params['TimeInForce']
    }
    fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce)

    #Cancel order
    cancel_parms = {
        "ClOrdID": fix_message_PerVolume.get_ClOrdID(),
        "Account": fix_message_PerVolume.get_parameter('Account'),
        "Side": fix_message_PerVolume.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_PerVolume.get_ClOrdID()
    }
    fix_cancel = FixMessage(cancel_parms)
    responce_cancel = fix_manager_qtwquod5.Send_OrderCancelRequest_FixMessage(fix_cancel)
    cancel_er_params = {
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        "OrdStatus": "4"
    }
    fix_verifier_ss.CheckExecutionReport(cancel_er_params, responce_cancel )
    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
