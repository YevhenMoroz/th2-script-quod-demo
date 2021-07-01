from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-3220"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "3"
    client = "MOClient"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew('fix-bs-eq-paris',
                                                                             'MOClient_PARIS', "XPAR", 3)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade('fix-bs-eq-paris', 'MOClient_PARIS', 'XPAR', 3,
                                                                      800, 1)

        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
        time.sleep(1)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion
    response = fix_message.pop('response')
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # # endregion
    # # region Book
    eq_wrappers.book_order(base_request, client, price,)
    # endregion
    time.sleep(10)
    # region Verify
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': '*',
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'NoRootMiscFeesList': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'}
        ],

        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '*',
        # 'RootSettlCurrAmt': '*',
        'RootOrClientCommission': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'RootOrClientCommissionCurrency': '*',
        'RootCommTypeClCommBasis': '*',
        'RootSettlCurrAmt': '*'

    }
    fix_verifier_ss = FixVerifier('fix-ss-back-office', case_id)
    fix_verifier_ss.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocTransType'])
    # endregion
    # region aprrove block
    eq_wrappers.approve_block(base_request)
    # endregion

    # Region Verify order
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Accepted')
    eq_wrappers.verify_block_value(base_request, case_id, 'Summary Status', '')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Matched')
    # endregion
