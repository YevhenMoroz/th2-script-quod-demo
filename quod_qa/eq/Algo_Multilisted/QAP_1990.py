import os
import logging
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager

logger = logging.getLogger(__name__)


def execute(report_id):


    try:
        # region Declarations
        qty = 3000
        price = 40
        client = "CLIENT2"
        timenow = datetime.utcnow()
        instrument = {
            'Symbol': 'FR0000066052_EUR',
            'SecurityID': 'FR0000066052',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
        sor_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': qty,
            'TimeInForce': 1,
            'OrdType': 1,
            'TransactTime': timenow.isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': 1008,
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
                }
            ]}
        # endregion
        # region Rules
        rule_manager = RuleManager()
        ioc_rule = rule_manager.add_NewOrdSingle_IOC('fix-bs-eq-paris', 'XPAR_CLIENT2', 'XPAR', True, qty, 40)
        # endregion
        # region Connectivity
        case_id = bca.create_event(os.path.basename(__file__), report_id)
        fix_manager_qtwquod5 = FixManager('gtwquod5', case_id)
        fix_verifier_ss = FixVerifier('gtwquod5', case_id)
        fix_verifier_paris = FixVerifier('fix-bs-eq-paris', case_id)
        # endregion

        fix_message = FixMessage(sor_params)
        fix_message.add_random_ClOrdID()
        sor_responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)

        time.sleep(1)
        # Check on ss
        er_params_new = {
            'ExecType': "0",
            'OrdStatus': '0',
            'TimeInForce': sor_params['TimeInForce'],
            'OrderID': sor_responce.response_messages_list[0].fields['OrderID'].simple_value
        }
        fix_verifier_ss.CheckExecutionReport(er_params_new, sor_responce, message_name='Check ER to SS',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        # Check on bs
        NOS_BS_params = {
            'OrderQty': qty,
            'Price': price,
            'ChildOrderID': '*',
            'TimeInForce': 3
        }
        fix_verifier_paris.CheckNewOrderSingle(NOS_BS_params, sor_responce, key_parameters=['Price', 'OrderQty'],
                                             message_name="Check 3rd child qty")

        ERTrade_BS_params = {
            'OrderQty': qty,
            'Price': price,
            'ExecType': 'F',
            'TimeInForce': NOS_BS_params['TimeInForce'],
            'ClOrdID': '*'
        }
        fix_verifier_paris.CheckExecutionReport(ERTrade_BS_params, sor_responce, key_parameters=['Price', 'OrderQty', 'ExecType'],
                                               message_name="Check 3rd child qty", direction="SECOND")
        # Check on ss
        er_params_trade = {
            'ExecType': "F",
            'OrdStatus': '2',
            'TimeInForce': sor_params['TimeInForce'],
            'OrderID': sor_responce.response_messages_list[0].fields['OrderID'].simple_value
        }
        fix_verifier_ss.CheckExecutionReport(er_params_trade, sor_responce, message_name='Check ER to SS',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])



    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(ioc_rule)