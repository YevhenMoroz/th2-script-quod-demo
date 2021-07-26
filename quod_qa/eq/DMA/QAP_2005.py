import logging
import os
import time
from copy import deepcopy
from datetime import datetime, date, timedelta

from quod_qa.wrapper.eq_wrappers import buy_connectivity, sell_connectivity
from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# need to modify
def execute(report_id, session_id):
    case_name = "QAP-2005"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = 20
    price2 = 19
    client = 'CLIENT_FIX_CARE'
    expireDate = date.today() + timedelta(2)

    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + "_PARIS", 'XPAR', price)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 2, client, 2, qty, 0, price)
    except:
        rule_manager.remove_rule(nos_rule)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion

    response = fix_message.pop('response')
    fix_message1 = FixMessage(fix_message)
    fix_manager = FixManager(sell_connectivity, case_id)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OrderCancelReplaceRequest(eq_wrappers.get_buy_connectivity(), client + "_PARIS", "XPAR",
                                                          True)
        fix_modify_message = deepcopy(fix_message1)
        fix_modify_message.change_parameters({'Price': price2})
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(rule)
    # endregion
    cl_order_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
    params = {
        'ExecType': '5',
        'OrdStatus': '0',
        'Side': '2',
        'TimeInForce': '0',
        'ClOrdID': cl_order_id,
        'OrigClOrdID': cl_order_id,
        'OrderQtyData': {'OrderQty': qty},
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'ExecBroker': '*',
        'Price': price2,
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'TransactTime': '*',
        'Text': 'order replaced',
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
        'SettlType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
    }
    fix_verifier_bo = FixVerifier(eq_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckExecutionReport(params, response, ['ClOrdID', 'ExecType'])
    # region Cancelling order

    try:
        rule = rule_manager.add_OrderCancelRequest(eq_wrappers.get_sell_connectivity(), client + "_PARIS",
                                                   "XPAR", True)
        eq_wrappers.cancel_order_via_fix(case_id, eq_wrappers.get_buy_connectivity(), cl_order_id, cl_order_id, client,
                                         1)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(rule)
    # endregion
    params = {
        'OrderQtyData': {'OrderQty': qty},
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': '2',
        'TimeInForce': '0',
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'OrigClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'LastQty': '*',
        'ExecBroker': '*',
        'OrderID': '*',
        'Price': price2,
        'TransactTime': '*',
        'Text': 'order canceled',
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
        'SettlType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
    }
    fix_verifier_bo.CheckExecutionReport(params, response, ['ClOrdID', 'ExecType'])

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
