import logging
import os
from copy import deepcopy
from datetime import datetime, timedelta
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


def execute(report_id, session_id):
    case_name = "QAP-3339"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "800"
    newQty = "100"
    price = "40"
    newPrice = "1"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
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
    # endregionA

    # region Create CO
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    response = fix_message.pop('response')
    # endregion
    # Amend fix order
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    eq_wrappers.manual_execution(base_request, str(int(qty) / 2), price)
    # endregion
    str1 = str(datetime.now().date() + timedelta(days=1)).replace('-', '')
    params = {
        'OrderQty': qty,
        'ExecType': 'F',
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
        'SettlDate': str1,
        'SettlType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'LastCapacity': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }
    fix_verifier_ss = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params1',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
    params['OrdStatus'] = '2'
    fix_verifier_ss = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params2',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
