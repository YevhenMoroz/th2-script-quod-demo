import logging

import quod_qa.wrapper.eq_fix_wrappers
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
import time
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1073"

    # region Declarations
    qty = "900"
    price = "40"
    newPrice = "1"
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
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
    # region Create CO
    fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    param_list = {'Price': newPrice}
    # region ManualExecute
    eq_wrappers.manual_execution(base_request, str(int((int(qty) / 2))), price)
    response = fix_message.pop('response')
    # print(fix_message['Price'])
    # Amend fix order
    fix_message1 = FixMessage(fix_message)
    quod_qa.wrapper.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message1, param_list, "PARIS_" + client)
    # endregion
    # region reject amend
    eq_wrappers.reject_order(lookup, qty, price)
    # endregion
    # Check on ss
    params = {
        'OrderQty': qty,
        'ExecType': 'F',
        'Account': client,
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
        'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'LastCapacity': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }
    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType'])
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'OrdStatus'])
    fix_verifier_ss = FixVerifier(quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType'])
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'OrdStatus'])
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType'], direction="SECOND")
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'OrdStatus'], direction="SECOND")

