import logging
import os
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)

def execute(report_id):

    # region Rules
    rule_manager = RuleManager()
    ocr_rule = rule_manager.add_OCR("fix-bs-eq-trqx")
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-trqx", 'TRQX_CLIENT2', 'TRQX', 35)

    # endregion

    try:
        # region Declarations
        qty = 3000
        price = 35
        client = "CLIENT2"
        timenow = datetime.utcnow()
        instrument ={
            'Symbol': 'DE0006228604_EUR',
            'SecurityID': 'DE0006228604',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XETR'
        }
        # endregion
        #region Connectivity
        case_id = bca.create_event(os.path.basename(__file__), report_id)
        fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
        fix_verifier_ss = FixVerifier('gtwquod5', case_id)
        fix_verifier_bs = FixVerifier('fix-bs-eq-trqx', case_id)
        #endregion
        twap_params = {
            'Account': client,
            'HandlInst': "2",
            'Side': "1",
            'OrderQty': qty,
            'TimeInForce': "0",
            'Price': price,
            'OrdType': "2",
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': "1005",
            'ExDestination': 'TRQX',
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'StartDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': timenow.strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'EndDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': (timenow + timedelta(minutes=3)).strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'Aggressivity',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '1'
                }
            ]
        }
        fix_message = FixMessage(twap_params)
        fix_message.add_random_ClOrdID()
        twap_responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)

        # Check on ss
        er_params_new = {
            'ExecType': "0",
            'OrdStatus': '0',
            'OrderID': twap_responce.response_messages_list[0].fields['OrderID'].simple_value
        }
        fix_verifier_ss.CheckExecutionReport(er_params_new, twap_responce)

        time.sleep(1)
        # Check BS orders
        NOS_BS_params1 = {
            'OrderQty': int(qty / 3),
            'Price': price,
            'ChildOrderID': '*'
        }
        fix_verifier_bs.CheckNewOrderSingle(NOS_BS_params1, twap_responce, key_parameters=['OrderQty'],
                                             message_name="Check 1st child qty")
        time.sleep(60)
        NOS_BS_params2 = {
            'OrderQty': int(qty / 3 * 2),
            'Price': price,
            'ChildOrderID': '*'
        }
        fix_verifier_bs.CheckNewOrderSingle(NOS_BS_params2, twap_responce, key_parameters=['Price', 'OrderQty'],
                                             message_name="Check 2nd child qty")
        time.sleep(60)
        NOS_BS_params3 = {
            'OrderQty': int(qty),
            'Price': price,
            'ChildOrderID': '*'
        }
        fix_verifier_bs.CheckNewOrderSingle(NOS_BS_params3, twap_responce, key_parameters=['Price', 'OrderQty'],
                                             message_name="Check 3rd child qty")

        TWAP_ER_SS_params = {
            'OrdStatus': 4,
            'OrderID': twap_responce.response_messages_list[0].fields['OrderID'].simple_value,
            'Price': price,
            'Text': 'reached end time',
            'CumQty': 0
        }
        fix_verifier_ss.CheckExecutionReport(TWAP_ER_SS_params, twap_responce)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(ocr_rule)



