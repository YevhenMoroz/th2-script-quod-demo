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
    case_name = "QAP-3293"

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
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # endregion
    param_list = {'Price': newPrice}
    response = fix_message.pop('response')
    # region check FIX CO
    params = {
        'OrderQty': qty,
        'ExecType': 'A',
        # 'Account': '*',
        'OrdStatus': 'A',
        # 'TradeDate': '*',
        'Side': 1,
        'Price': price,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        # 'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        # 'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        # 'SettlDate': '*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        # 'LastCapacity': '*',
        # 'ExDestination': '*',
        # 'GrossTradeAmt': '*',
        'ExpireDate': '*',
        # 'ChildOrderID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion

    # region check_out order
    eq_wrappers.check_out_order(base_request)
    # endregion
    # region check_out order
    eq_wrappers.verify_value(base_request, case_id, 'IsLocked', 'Yes', False)
    # endregion
    time.sleep(20)
    # region CancelOrderReplaceRequest sent
    eq_wrappers.amend_order_via_fix(case_id, fix_message, param_list)
    # endregion
    # check tag 58
    params = {
        # 'OrderQty': qty,
        # 'ExecType': 'A',
        # 'Account': '*',
        'OrdStatus': '0',
        # 'TradeDate': '*',
        # 'Side': 1,
        # 'Price': price,
        # 'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        # 'ExecID': '*',
        # 'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        # 'AvgPx': '*',
        # 'SettlDate': '*',
        # 'Currency': '*',
        # 'HandlInst': '*',
        # 'LeavesQty': '*',
        # 'CumQty': '*',
        # 'LastPx': '*',
        # 'OrdType': '*',
        # 'LastMkt': '*',
        # 'OrderCapacity': '*',
        # 'QtyType': '*',
        # 'SettlDate': '*',
        # 'SettlType': '*',
        # 'NoParty': '*',
        # 'Instrument': '*',
        'Text': '11629 Order is in locked state',
        # 'header': '*',
        # 'LastCapacity': '*',
        # 'ExDestination': '*',
        # 'GrossTradeAmt': '*',
        # 'ExpireDate': '*',
        # 'ChildOrderID': '*'
        'OrigClOrdID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckCancelReject(params, response, message_name='Check params',
                                      key_parameters=['ClOrdID', 'OrdStatus'])
    # endregion

    # check in Order
    eq_wrappers.check_in_order(base_request)
    time.sleep(20)
    # endregion

    # region resend ORDER_CANCEL_REPLACE_REQUEST
    eq_wrappers.amend_order_via_fix(case_id, fix_message, param_list)
    # endregion

    # region  accept modify
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion

    # region check isLocked
    verifier = Verifier(case_id)
    print(type(eq_wrappers.get_is_locked(base_request)))
    verifier.set_event_name("Check value")
    verifier.compare_values("IsLocked from View", eq_wrappers.get_is_locked(base_request), ''),
    verifier.verify()
    # endregion

    # region verify fix message

    params = {
        'OrderQty': qty,
        'ExecType': 5,
        # 'Account': '*',
        'OrdStatus': 0,
        # 'TradeDate': '*',
        'Side': 1,
        'Price': newPrice,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        # 'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        # 'LastCapacity': '*',
        # 'ExDestination': '*',
        # 'GrossTradeAmt': '*',
        # 'ExpireDate': '*',
        # 'ChildOrderID': '*',
        'OrigClOrdID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion
