import test_framework.old_wrappers.eq_fix_wrappers
from custom.verifier import Verifier
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
import logging
from rule_management import RuleManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def execute(report_id,session_id):
    case_name = "QAP-2780"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    client = "MOClient"

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create DMA
    rule_manager = RuleManager()
    trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(
        test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(), client + "_PARIS", "XPAR",
        int(price), int(qty), 0)
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 1, price)
    response = fix_message.pop('response')
    rule_manager.remove_rule(trade_rule)
    # endregion
    # region Verify
    fix_verifier_buy = FixVerifier(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), case_id)
    params = {
        'Account': client,
        'OrderQty': qty,
        'ExecType': 'F',
        'ExpireDate': '*',
        'OrdStatus': '2',
        'TradeDate': '*',
        'Price':price,
        'Side': 1,
        'TimeInForce': 1,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'SecondaryExecID': '*',
        'Text': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LastExecutionPolicy': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SecondaryOrderID': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'SettlType': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
    }
    fix_verifier_buy.CheckExecutionReport(params,response)

    # endregion
    # region Book
    eq_wrappers.book_order(base_request,client,price)
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "Booked")
    # endregion
    # region View orders
    response=eq_wrappers.view_orders_for_block(base_request,1)
    # endregion
    # region Verify
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View", eq_wrappers.get_order_id(base_request), response[0]["middleOffice.orderId"])
    verifier.verify()
    # endregion

