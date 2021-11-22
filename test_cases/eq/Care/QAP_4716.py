import logging

import test_cases.wrapper.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4716"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "40"
    client = "CLIENT_FIX_CARE_WB"
    account = "CLIENT_FIX_CARE_WB_SB1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    no_allocs = [
        {
            'AllocAccount': account,
            'AllocQty': qty
        }
    ]
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create order via fix
    fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price, no_allocs)
    response = fix_message['response']
    # endregion
    eq_wrappers.accept_order('VETO', qty, price)
    # Cancel order via hot key
    # params = {
    #     'OrderQty': qty,
    #     'ExecType': '0',
    #     'Account': '*',
    #     'OrdStatus': 0,
    #     'Side': 1,
    #     'Price': price,
    #     'TimeInForce': 0,
    #     'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
    #     'ExecID': '*',
    #     'LastQty': '*',
    #     'OrderID': '*',
    #     'TransactTime': '*',
    #     'AvgPx': '*',
    #     'SettlDate': '*',
    #     'Currency': '*',
    #     'HandlInst': '*',
    #     'LeavesQty': '*',
    #     'CumQty': '*',
    #     'LastPx': '*',
    #     'OrdType': '*',
    #     'OrderCapacity': '*',
    #     'QtyType': '*',
    #     'SettlDate': '*',
    #     'SettlType': '*',
    #     'NoParty': '*',
    #     'Instrument': '*',
    #     'header': '*',
    #     'ExpireDate': '*'
    # }
    # fix_verifier_ss = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    # fix_verifier_ss.CheckExecutionReport(params, response, message_name='Check params',
    #                                      key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
    eq_wrappers.verify_order_value(base_request, case_id, 'Account ID', 'CLIENT_FIX_CARE_WB_SB1')
    eq_wrappers.verify_order_value(base_request, case_id, 'Wash Book', 'CareWB', False)
