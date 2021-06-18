import time

from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-3388"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "50"
    client = "CLIENTYMOROZ"
    account = "CLIENT_YMOROZ_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-buy-317ganymede-standard',
                                                                             'CLIENTYMOROZ_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade('fix-buy-317ganymede-standard',
                                                                      'CLIENTYMOROZ_PARIS', 'XPAR',
                                                                      int(price), int(qty), 1)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    # endregion
    # region Approve
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    # endregion
    # region Allocate
    arr_allocation_param = [{"Security Account": account, "Alloc Qty": qty}]
    eq_wrappers.allocate_order(base_request, arr_allocation_param)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Summary Status", "MatchedAgreed")
    eq_wrappers.verify_allocate_value(base_request, case_id, "Status", "Affirmed")
    eq_wrappers.verify_allocate_value(base_request, case_id, "Match Status", "Matched")
    # endregion
    # region Amend allocate
    eq_wrappers.amend_allocate(base_request, agreed_price=str(int(price) + 1))
    # endregion
    # region Verify
    params = {
        'Account': client,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'AllocQty': qty,
        'AllocAccount': account,
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'BookID': '*',
        'header': '*',
        'AllocInstructionMiscBlock1': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'MatchStatus': '*',
        'ConfirmStatus': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'ReportedPx': '*',
        'CpctyConfGrp': '*',
        'ConfirmTransType': '1',
        'ConfirmID': '*'
    }
    fix_verifier_ss = FixVerifier('fix-sell-317-backoffice', case_id)
    fix_verifier_ss.CheckConfirmation(params, response, ['NoOrders','ConfirmTransType','Account'])
    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'BookID': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '2',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '1',
        'ReportedPx': '*',
        'AllocInstructionMiscBlock1': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': account,
                'AllocPrice': str(int(price) + 1),
                'AllocQty': qty,

            }
        ],
    }
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType','Account'])
    # endregion
