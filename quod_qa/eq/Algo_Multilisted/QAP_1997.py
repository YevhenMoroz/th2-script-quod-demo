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
        price = 35
        client = "CLIENT2"
        timenow = datetime.utcnow()
        instrument = {
            'Symbol': 'FR0000066052_EUR',
            'SecurityID': 'FR0000066052',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
        multilisting_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': qty,
            'TimeInForce': 3,
            'OrdType': 2,
            'TransactTime': timenow.isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': 1008,
            'Price': price,
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
        # endregion
        # region Connectivity
        case_id = bca.create_event(os.path.basename(__file__), report_id)
        fix_manager_qtwquod5 = FixManager('fix-ss-310-columbia-standart', case_id)
        fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
        # endregion

        fix_message_multilisting = FixMessage(multilisting_params)
        fix_message_multilisting.add_random_ClOrdID()
        responce = fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message_multilisting)

        time.sleep(1)
        # Check on ss
        er_params_new = {
            'ExecID': '*',
            'OrderQty': qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': multilisting_params['Side'],
            'AvgPx': '0',
            'OrdStatus': '4',
            'SettlDate': '*',
            'Currency': multilisting_params['Currency'],
            'TimeInForce': multilisting_params['TimeInForce'],
            'ExecType': "4",
            'HandlInst': multilisting_params['HandlInst'],
            'LeavesQty': '0',
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': multilisting_params['OrdType'],
            'ClOrdID': fix_message_multilisting.get_ClOrdID(),
            'Text': 'no liquidity found',
            'OrderCapacity': multilisting_params['OrderCapacity'],
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'SettlType': '*',
            'Price': price,
            'TargetStrategy': multilisting_params['TargetStrategy'],
            'Instrument': instrument
        }
        fix_verifier_ss.CheckExecutionReport(er_params_new, responce, message_name='Check ER to SS',
                                             key_parameters=['OrderID', 'OrdStatus', 'ExecType'])

    except Exception:
        logger.error("Error execution", exc_info=True)
