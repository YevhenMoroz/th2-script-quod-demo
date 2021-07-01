import logging
import os
from datetime import datetime, date, timedelta
import time

from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from quod_qa.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-2008"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    qty2 = "1500"
    price = 3
    expireDate = date.today() + timedelta(2)
    time1 = datetime.utcnow().isoformat()
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             'XPAR_CLIENT1', "XPAR", price)

        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 2, 'CLIENT1', 2, qty, 6, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    response = fix_message.pop('response')
    # region Check
    time.sleep(1)
    params = {
        'OrderQty': qty,
        'ExecType': 0,
        'OrdStatus': 0,
        'Side': 2,
        'Price': price,
        'TimeInForce': 6,
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
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        'Text':'*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        ''
        'header': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion
    # endregion

    # region Amend order
    eq_wrappers.amend_order_via_fix(case_id, fix_message, {'OrderQty': qty2})
    # endregion

    # region Check values after Amending
    params = {
        'OrderQty': qty2,
        'ExecType': 5,
        'Account': '*',
        'OrdStatus': 1,
        'TradeDate': '*',
        'Side': 1,
        'Price': price,
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
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'LastCapacity': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss = FixVerifier(eq_wrappers.get_buy_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion

    # region Cancelling order
    eq_wrappers.cancel_order_via_fix(case_id, session_id, eq_wrappers.get_cl_order_id(base_request),
                                     str(int(eq_wrappers.get_cl_order_id(base_request)) + 1), 'CLIENT1', 2)
    # endregion

    # region Check values after Cancel
    params = {
        'OrderQty': qty,
        'ExecType': 5,
        'OrdStatus': 1,
        'Side': 1,
        'Price': price,
        'TimeInForce': 6,
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
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SettlDate': '*',
        # 'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'ExpireDate': '*',
    }
    fix_verifier_ss = FixVerifier(eq_wrappers.get_buy_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus', 'Price'])
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
