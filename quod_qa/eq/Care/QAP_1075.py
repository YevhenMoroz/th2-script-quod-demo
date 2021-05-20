import logging
import os
from copy import deepcopy
from datetime import datetime
from th2_grpc_act_gui_quod import order_ticket_service

from custom.verifier import Verifier
from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails, CancelOrderDetails
from custom.basic_custom_actions import create_event, timestamps
import time
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_manager import FixManager
from rule_management import RuleManager
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

def execute(report_id):
    case_name = "QAP-1074"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    newQty = "100"
    price = "40"
    newPrice = "1"
    lookup = "PROL"
    client = "CLIENTSKYLPTOR"
    # endregion
    list_param = {'qty': qty, 'Price': newPrice}
    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    param_list = {'Price': newPrice}
    # region ManualExecute
    eq_wrappers.manual_execution(base_request, str(int(qty)), price)
    response = fix_message.pop('response')
    # print(fix_message['Price'])
    # Amend fix order
    eq_wrappers.amend_order_via_fix(fix_message, case_id, param_list)
    # endregion
    print(fix_message['Price'])
    # region accept amend
    eq_wrappers.reject_order(lookup, qty, price)
    # endregion
    time.sleep(1)
    # Check on ss
    # print(eq_wrappers.get_order_id(base_request))
    # print(fix_message['ClOrdID'])
    # fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    # er_params_new = {
    #     'ExecType': "F",
    #     'OrdStatus': '2',
    #     'TimeInForce': 0,
    #     'ClOrdID': fix_message['ClOrdID']
    # }
    # fix_verifier_ss.CheckNewOrderSingle(er_params_new, response, key_parameters=['ClOrdID'])
    params = {
        'ExecType': 'F',
        'OrdStatus': '1',
        'Side': 2,
        'Price': price,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
    }
    print(response.response_messages_list[0].fields['ClOrdID'].simple_value)
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])