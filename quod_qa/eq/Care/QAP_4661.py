import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_fix_wrappers, eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    qty = "1300"
    client = "CLIENT_iPal"
    handle_inst = 3
    side = 1
    ord_type = 4
    case_name = "QAP-4661"
    tif = 1
    case_id = create_event(case_name, report_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    precondition_fix_message = eq_fix_wrappers.create_order_via_fix(case_id, handle_inst, side, client, ord_type, qty,
                                                                    tif,
                                                                    stop_price=300, price=300)
    response = precondition_fix_message.pop("response")
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    eq_wrappers.accept_order("VETO", qty, "300")
    eq_fix_wrappers.amend_order_via_fix(case_id, precondition_fix_message,
                                        parametr_list={"TimeInForce": 0, "StopPx": 200})
    eq_wrappers.accept_modify("VETO", qty, "300")
    params = {
        'OrderQty': "*",
        'OrdStatus': '0',
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'SettlType': '0',
        "StopPx": 200,
        "ExecType": 5,
        "NoParty": "*",
        "Account": "*",
        "ExecID": "*",
        "LastQty": "*",
        "OrderID": "*",
        "TransactTime": "*",
        "Side": "*",
        "AvgPx": "*",
        "SettlDate": "*",
        "Currency": "*",
        "HandlInst": "*",
        "LeavesQty": "*",
        "CumQty": "*",
        "LastPx": "*",
        "OrdType": "*",
        "QtyType": "*",
        "Price": "*",
        "Instrument": "*",
        "OrigClOrdID": "*"

    }
    fix_verifier_bs = FixVerifier(eq_fix_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_bs.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'OrdStatus', "ExecType"])
