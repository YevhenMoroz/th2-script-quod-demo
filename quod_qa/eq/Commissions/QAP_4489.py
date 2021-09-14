import time

from custom.verifier import Verifier, VerificationMethod
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import set_session_id, get_base_request, call
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4489"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    lookup = "VETO"
    client = "CLIENT_FEES_1"
    account = "CLIENT_FEES_1_SA1"
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

        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 2, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region book_order
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region approve_block
    eq_wrappers.approve_block(base_request)
    # endregion
    # region allocate_order
    param = [{"Security Account": account, "Alloc Qty": qty}
             ]
    eq_wrappers.allocate_order(base_request, param)
    # endregion
    # region Verify
    params = {
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': qty,
        'AllocAccount': client,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'NoMiscFees': [
            {'MiscFeeAmt': '450',
             'MiscFeeCurr': '*',
             'MiscFeeType': '22'}
        ],
        'AllocInstructionMiscBlock1': '*',
        'CommissionData': {
            'CommissionType': '*',
            'CommCurrency': '*',
            'Commission': '*'},
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_bo = FixVerifier(eq_wrappers.get_bo_connectivity(), case_id)
    fix_verifier_bo.CheckConfirmation(params, response, ['NoOrders'])
    # endregion
