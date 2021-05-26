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
        qty = 1300
        price = 40
        client = "CLIENT2"
        timenow = datetime.utcnow()
        instrument = {
            'Symbol': 'FR0000125007_EUR',
            'SecurityID': 'FR0000125007',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
        multilisting_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': qty,
            'TimeInForce': 6,
            'ExpireDate': (timenow + timedelta(days=2)).strftime("%Y%m%d"),
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
        ioc_rule = rule_manager.add_NewOrdSingle_IOC('fix-bs-310-columbia', 'XPAR_CLIENT2', 'XPAR', True, qty, 40)
        # endregion
        # region Connectivity
        case_id = bca.create_event(os.path.basename(__file__), report_id)
        fix_manager_qtwquod5 = FixManager('fix-ss-310-columbia-standart', case_id)
        fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
        fix_verifier_paris = FixVerifier('fix-bs-310-columbia', case_id)
        # endregion

        fix_message_multilisting = FixMessage(multilisting_params)
        fix_message_multilisting.add_random_ClOrdID()
        responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_multilisting)

        time.sleep(1)
        # Check on ss
        er_params_new = {
        'ExecID': '*',
        'OrderQty': multilisting_params['OrderQty'],
        'NoStrategyParameters': '*',
        'ExpireDate': '*',
        'LastQty': '0',
        'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': multilisting_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'ExecType': "0",
        'HandlInst': multilisting_params['HandlInst'],
        'LeavesQty': multilisting_params['OrderQty'],
        'NoParty': '*',
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(), 
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'QtyType': '0',
        'ExecRestatementReason': '*',
        'SettlType': '0',
        'TargetStrategy': multilisting_params['TargetStrategy'],
        'Instrument': multilisting_params['Instrument']
        }
        fix_verifier_ss.CheckExecutionReport(er_params_new, responce, message_name='Check ER to SS',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
        # Check on bs
        NOS_BS_params = {
        'NoParty': '*',
        'Account': multilisting_params['Account'],       
        'OrderQty': multilisting_params['OrderQty'],
        'OrdType': multilisting_params['OrdType'],
        'ClOrdID': fix_message_multilisting.get_ClOrdID(),
        'OrderCapacity': multilisting_params['OrderCapacity'],
        'TransactTime': '*',
        'ChildOrderID': '*',
        'Side': multilisting_params['Side'],
        'Price': price,
        'SettlDate': '*',
        'Currency': multilisting_params['Currency'],
        'TimeInForce': multilisting_params['TimeInForce'],
        'Instrument': '*',
        'HandlInst': '1',
        'ExDestination': multilisting_params['Instrument']['SecurityExchange']
        }
        fix_verifier_paris.CheckNewOrderSingle(NOS_BS_params, responce, key_parameters=['Price', 'OrderQty'],
                                             message_name="Check 3rd child qty")

        ERTrade_BS_params = {
            'OrderQty': qty,
            'Price': price,
            'ExecType': 'F',
            'TimeInForce': NOS_BS_params['TimeInForce'],
            'ClOrdID': '*'
        }
        fix_verifier_paris.CheckExecutionReport(ERTrade_BS_params, responce, key_parameters=['Price', 'OrderQty', 'ExecType'],
                                               message_name="Check 3rd child qty", direction="SECOND")
        # Check on ss
        er_params_trade = {
            'ExecType': "F",
            'OrdStatus': '2',
            'TimeInForce': multilisting_params['TimeInForce'],
            'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value
        }
        fix_verifier_ss.CheckExecutionReport(er_params_trade, responce, message_name='Check ER to SS',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])



    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(ioc_rule)