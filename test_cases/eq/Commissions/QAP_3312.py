import time

from custom.verifier import Verifier, VerificationMethod
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from custom import basic_custom_actions as bca
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import set_session_id, get_base_request, call
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3312"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "1000"
    price = "400"
    lookup = "VETO"
    client = "CLIENT_COMM_1"
    account = 'CLIENT_COMM_1_SA3'
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                      client + '_PARIS', 'XPAR',
                                                                      float(price), int(qty), 1)
        # checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(report_id))
        # checkpoint_id1 = checkpoint_response1.checkpoint
        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 2, client, 2, qty, 0, price,
                                                       [
                                                           {
                                                               'AllocAccount': account,
                                                               'AllocQty': qty
                                                           }
                                                       ]
                                                       )
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion
    # region Verify
    params = {
        'OrderQty': qty,
        'ExecType': 'F',
        'OrdStatus': '2',
        'Account': 'CLIENT_COMM_1',
        'Side': 2,
        'Text': '*',
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'LastExecutionPolicy': '*',
        'TradeDate': '*',
        'AvgPx': '*',
        'ExpireDate': '*',
        'SettlDate': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'SettlType': '*',
        'OrdType': '*',
        'LastMkt': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'SecondaryOrderID': '*',
        'NoParty': '*',
        'Instrument': '*',
        'SecondaryExecID': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*'
    }
    fix_verifier_bo = FixVerifier(eq_wrappers.get_sell_connectivity(), case_id)
    fix_verifier_bo.CheckExecutionReport(params, response, ['ClOrdID', 'ExecType', 'OrdStatus'])
    # endregion
