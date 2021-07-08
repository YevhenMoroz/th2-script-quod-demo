import logging
import os
from copy import deepcopy
from datetime import datetime, date, timedelta

from quod_qa.wrapper.eq_wrappers import buy_connectivity
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
    client = 'CLIENT1'
    expireDate = date.today() + timedelta(2)
    time = datetime.utcnow().isoformat()
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
                                                                             'XPAR_' + client, 'XPAR', price)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price)
    except:
        rule_manager.remove_rule(nos_rule)
    finally:
        rule_manager.remove_rule(nos_rule)
    # endregion

    response = fix_message.pop('response')
    fix_message1=FixMessage(fix_message)
    fix_manager = FixManager(buy_connectivity, case_id)
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_OCRR(eq_wrappers.get_buy_connectivity())
        fix_modify_message = deepcopy(fix_message1)
        fix_modify_message.change_parameters({'Price': 3})
        fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(rule)
    # endregion
    params = {
        'OrderQty': qty,
        'ExecType': '4',
        'OrdStatus': '4',
        'Side': 2,
        'TimeInForce': 6,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'Text': '*',
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
    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
    # region Cancelling order
    # try:
    #     rule_manager = RuleManager()
    #     nos_rule_amend = rule_manager.add_OCR(eq_wrappers.get_buy_connectivity())
    #     eq_wrappers.cancel_order_via_fix(case_id, session_id, eq_wrappers.get_cl_order_id(base_request),
    #                                      str(int(eq_wrappers.get_cl_order_id(base_request)) + 1), client, 1)
    # except:
    #     rule_manager.remove_rule(nos_rule_amend)
    # # endregion
    # params = {
    #     'OrderQty': qty,
    #     'ExecType': '4',
    #     'OrdStatus': '4',
    #     'Side': 2,
    #     'TimeInForce': 6,
    #     'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
    #     'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
    #     'ExecID': '*',
    #     'LastQty': '*',
    #     'OrderID': '*',
    #     'TransactTime': '*',
    #     'Text': '*',
    #     'AvgPx': '*',
    #     'SettlDate': '*',
    #     'Currency': '*',
    #     'HandlInst': '*',
    #     'LeavesQty': '*',
    #     'CumQty': '*',
    #     'LastPx': '*',
    #     'OrdType': '*',
    #     'LastMkt': '*',
    #     'OrderCapacity': '*',
    #     'QtyType': '*',
    #     'SettlType': '*',
    #     'SecondaryOrderID': '*',
    #     'NoParty': '*',
    #     'Instrument': '*',
    # }
    # fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    # fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
    #                                      key_parameters=['ClOrdID', 'ExecType'])
    #
    # logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
