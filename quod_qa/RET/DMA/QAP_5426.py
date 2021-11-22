import logging
import os
from copy import deepcopy
from datetime import datetime, date, timedelta
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps

from quod_qa.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_5426"
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

    response = fix_manager_315.Send_NewOrderSingle_FixMessage(fix_message)
    # end region

    # region Check on ss
    fix_verifier_ss = FixVerifier("fix-ss-315-luna-standart", case_id_1)
    er_params = {
        'ReplyReceivedTime': '*',
        'Account': '*',
        'ExecID': '*',
        'OrderQty': 100,
        'ExpireDate': '*',
        'LastQty': '*',
        'OrderID': response.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': 2,
        'AvgPx': '*',
        'OrdStatus': 0,
        'SettlDate': '*',
        'Currency': 'INR',
        'TimeInForce': 0,
        'ExecType': 0,
        'HandlInst': '*',
        'NoParty': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': 2,
        'ClOrdID': fix_message.get_ClOrdID(),
        'SecondaryOrderID': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlType': '*',
        'Price': 1,
        'Instrument': fix_params["Instrument"],
    }
    fix_verifier_ss.CheckExecutionReport(er_params, response, message_name='Check ER to SS',
                                         key_parameters=['OrdStatus'])
    # end region

    # region Modify order
    case_id_2 = bca.create_event("Modify Order", case_id_1)
    # Send OrderCancelReplaceRequest
    fix_modify_message = deepcopy(fix_message)
    fix_modify_message.change_parameters({'Price': '30'})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    amend_response = fix_manager_315.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_2)
    # end region

    fix_verifier_after_amend = FixVerifier("fix-ss-315-luna-standart", case_id_1)
    er_params_new = {
        'ReplyReceivedTime': '*',
        'Account': '*',
        'ExecID': '*',
        'OrderQty': 100,

        'LastQty': '*',
        'OrderID': response.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'Side': 2,
        'AvgPx': '*',
        'OrdStatus': 0,
        'SettlDate': '*',
        'Currency': 'INR',
        'TimeInForce': 0,
        'ExecType': 5,
        'HandlInst': '*',
        'NoParty': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': 2,
        'ClOrdID': fix_message.get_ClOrdID(),
        'SecondaryOrderID': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlType': '*',
        'Price': 30,
        'Instrument': fix_params["Instrument"],
        'OrigClOrdID': '*'
    }
    fix_verifier_after_amend.CheckExecutionReport(er_params_new, amend_response, message_name='Check ER to SS',
                                                  key_parameters=['Price'])

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
