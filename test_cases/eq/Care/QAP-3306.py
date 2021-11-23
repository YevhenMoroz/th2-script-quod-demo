import logging

from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules import trades_blotter_wrappers
from win_gui_modules.common_wrappers import GridScrollingDetails
from win_gui_modules.order_book_wrappers import ManualExecutingDetails

from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3306"
    # region Declarations
    qty_third = "100"
    qty_second_order = '70'
    qty_first_order = '30'
    price = "40"
    lookup = "EUREX"
    client = "MOClient"
    last_mkt = "XASE"
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

    # region Create CO orders
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty_first_order, 0, price)
    scrolling_details = GridScrollingDetails(ScrollingOperation.UP, 3, base_request)
    order_book_service = Stubs.win_act_order_book
    call(order_book_service.orderBookGridScrolling, scrolling_details.build())
    eq_wrappers.accept_order(lookup, qty_first_order, price)
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty_second_order, 0, price)
    order_book_service = Stubs.win_act_order_book
    call(order_book_service.orderBookGridScrolling, scrolling_details.build())
    eq_wrappers.accept_order(lookup, qty_second_order, price)
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty_third, 0, price)
    order_book_service = Stubs.win_act_order_book
    call(order_book_service.orderBookGridScrolling, scrolling_details.build())
    eq_wrappers.accept_order(lookup, qty_third, price)
    response = fix_message.pop('response')
    # endregion

    # region Manual Cross
    eq_wrappers.manual_cross_orders(base_request, qty_first_order, price, [1, 3], last_mkt)
    eq_wrappers.manual_cross_orders(base_request, qty_second_order, price, [1, 2], last_mkt)
    # endregion
    params = {
        'OrderQty': qty_third,
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
    fix_verifier_ss = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
    params['OrdStatus'] = '2'
    fix_verifier_ss.CheckExecutionReport(params, response, key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])
