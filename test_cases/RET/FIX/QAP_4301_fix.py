import os
import logging
from datetime import datetime, date, timedelta
from copy import deepcopy

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps

from win_gui_modules.utils import set_session_id
from win_gui_modules.wrappers import set_base

from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = os.path.basename(__file__)

    seconds, nanos = timestamps()  # Store case start time

    connectivity_sell_side = "fix-ss-310-columbia-standart"

    # region Declarations
    qty = ["1300", "1500"]
    price = "20"
    expire_date = date.today() + timedelta(2)
    # endregion

    # region Open FE
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    # work_dir = Stubs.custom_config['qf_trading_fe_folder']
    # username = Stubs.custom_config['qf_trading_fe_user']
    # password = Stubs.custom_config['qf_trading_fe_password']
    #
    # if not Stubs.frontend_is_open:
    #     prepare_fe(case_id, session_id, work_dir, username, password)
    # else:
    #     get_opened_fe(case_id, session_id)
    # endregion

    # region Create order via FIX according to 1st, 2nd and 3rd steps
    fix_manager_310 = FixManager(connectivity_sell_side, case_id)

    fix_params = {
        'Account': "CLIENT1",
        'HandlInst': "1",
        'Side': "2",
        'OrderQty': qty[0],
        'TimeInForce': "6",
        'ExpireDate': expire_date.strftime("%Y%m%d"),
        'OrdType': "2",
        'Price': price,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': {
            'Symbol': 'GB00B0J6N107_GBP',
            'SecurityID': 'GB00B0J6N107',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XLON'
        },
        'Currency': 'GBP'
    }

    fix_message = FixMessage(fix_params)
    fix_message.add_random_ClOrdID()
    response = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message, case=case_id)
    # end region

    # region Check order via FIX on sell side according to 4th step
    verify_params = {
        'ExecID': "*",
        'OrderQty': qty[0],
        'ExpireDate': expire_date.strftime("%Y%m%d"),
        'LastQty': "*",
        'OrderID': "*",
        'TransactTime': "*",
        'ExecType': '0',
        'HandlInst': '1',
        'LastPx': '0',
        'OrdType': "2",
        'LeavesQty': '1300',
        'NoParty': '*',
        'CumQty': '0',
        'OrdStatus': '0',
        'SettlDate': '*',
        'Currency': 'GBP',
        'Side': 2,
        'AvgPx': 0,
        'Price': price,
        'TimeInForce': 6,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'SecondaryOrderID': "*",
        'LastMkt': "CHIX",
        'OrderCapacity': "A",
        'QtyType': "0",
        'Instrument': {
            'Symbol': 'GB00B0J6N107_GBP',
            'SecurityID': 'GB00B0J6N107',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XLON'
        },
    }
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(verify_params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
    # endregion

    # region Amend order via FIX: Send OrderCancelReplaceRequest according to 5th step
    fix_modify_message = deepcopy(fix_message)
    fix_modify_message.change_parameters({'OrderQty': qty[1]})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, message_name='Amend order')
    # endregion

    # region Cancel order via FIX according to 6th step
    cancel_params = {
        "ClOrdID": fix_message.get_ClOrdID(),
        "Account": fix_message.get_parameter('Account'),
        "Side": fix_message.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message.get_ClOrdID()
    }
    fix_cancel = FixMessage(cancel_params)
    response_cancel = fix_manager_310.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id)
    # endregion

    # region Verify cancel via FIX
    verify_cancel_param = {
        'Side': fix_message.get_parameter('Side'),
        'Account': fix_message.get_parameter('Account'),
        'ClOrdID': fix_message.get_ClOrdID(),
        'TransactTime': '*',
        'OrigClOrdID': fix_message.get_ClOrdID()
    }
    fix_verifier_ss.CheckOrderCancelRequest(verify_cancel_param, response_cancel, direction='SECOND',
                                            case=case_id,
                                            message_name='SS FIXSELLQUOD5 sent 35=F Cancel',
                                            key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
