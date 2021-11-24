import logging
import os
from copy import deepcopy
from datetime import datetime, date, timedelta
from custom import basic_custom_actions as bca, verifier
from custom.basic_custom_actions import timestamps

from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_5425"
    seconds, nanos = timestamps()  # Store case start time

    connectivity_sell_side = "fix-ss-315-luna-standart"

    # region Declarations
    expire_date = date.today() + timedelta(2)
    # endregion

    # region Open FE
    case_id_1 = bca.create_event(os.path.basename(__file__), report_id)

    fix_manager_315 = FixManager(connectivity_sell_side, case_id_1)

    # region Create order via FIX Pre-Condition
    fix_params = {
        'Account': "HAKKIM",
        'HandlInst': "2",
        'Side': "2",
        'OrderQty': "100",
        'TimeInForce': "0",
        'ExpireDate': expire_date.strftime("%Y%m%d"),
        'OrdType': "2",
        'Price': "1",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'INE467B01029',
            'SecurityID': '532540',
            'SecurityIDSource': '8',
            'SecurityExchange': 'XBOM'
        },
        'Currency': 'INR',
    }

    fix_message = FixMessage(fix_params)

    fix_message.add_random_ClOrdID()

    fix_manager_315.Send_NewOrderSingle_FixMessage(fix_message)
    # end region

    # region Create order via FIX step 1
    fix_params_step1 = {
        'Account': "HAKKIM",
        'HandlInst': "1",
        'Side': "1",
        'OrderQty': "500",
        'TimeInForce': "3",
        'ExpireDate': expire_date.strftime("%Y%m%d"),
        'OrdType': "2",
        'Price': "1",
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'INE467B01029',
            'SecurityID': '532540',
            'SecurityIDSource': '8',
            'SecurityExchange': 'XBOM',
            'SecurityType': 'CS'
        },
        'Currency': 'INR',
    }
    fix_message_step1 = FixMessage(fix_params_step1)
    fix_message_step1.add_random_ClOrdID()

    response = fix_manager_315.Send_NewOrderSingle_FixMessage(fix_message_step1)
    print(response)
    # end region

    # region Check on ss
    fix_verifier_ss = FixVerifier("fix-ss-315-luna-standart", case_id_1)
    er_params_new = {
        'Account': '*',
        'ExecID': '*',
        'OrderQty': 500,
        'ExpireDate': '*',
        'LastQty': '*',
        'OrderID': response.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': 1,
        'AvgPx': '*',
        'OrdStatus': 1,
        'LastExecutionPolicy': '*',
        'SettlDate': '*',
        'Currency': 'INR',
        'TimeInForce': 3,
        'TradeDate': '*',
        'ExecType': "F",
        'HandlInst': '*',
        'NoParty': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': 2,
        'ClOrdID': fix_message_step1.get_ClOrdID(),
        'SecondaryOrderID': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'Price': 1,
        'Instrument': fix_params_step1["Instrument"],
        'MultiLegReportingType': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }
    fix_verifier_ss.CheckExecutionReport(er_params_new, response, message_name='Check ER to SS',
                                         key_parameters=['OrdStatus', 'ExecType'])
    # end region


    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
