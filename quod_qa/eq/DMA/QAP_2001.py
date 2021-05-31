import logging
import os
from datetime import datetime

from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2001"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "900"
    client = "CLIENTYMOROZ"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    price = 20
    # endregion

    # region Create and execute order via FIX
    try:
        rule_manager = RuleManager()
        rule = rule_manager.add_NewOrdSingle_Market("fix-bs-310-columbia", client + "_PARIS", "XPAR", True, int(int(qty)/2),
                                                    float(price))
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 2, client, 1, qty, 3)
        response = fix_message.pop('response')
    finally:
        rule_manager.remove_rule(rule)

    # endregion

    # region Check values in OrderBook
    params = {
        'Account': client,
        'OrderQty': qty,
        'ExecType': 'F',
        'OrdStatus': '1',
        'Side': 2,
        'Text': '*',
        'TimeInForce': 3,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'LastExecutionPolicy': '*',
        'TradeDate':'*',
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
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }

    fix_verifier_ss = FixVerifier('fix-ss-310-columbia-standart', case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])

    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
