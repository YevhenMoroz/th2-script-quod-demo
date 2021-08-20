import logging
import time

import quod_qa.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3536"
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_COUNTERPART"
    lookup = "VETO"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    bo_connectivity = quod_qa.wrapper.eq_fix_wrappers.get_bo_connectivity()

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # region Create Order
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            int(price), int(qty), 1)
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client + "_PARIS", 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Create order via FE
    eq_wrappers.create_order(base_request, qty, client, lookup, "Limit", is_care=True,recipient=username,
                                           price=price, recipient_user=True)
    # endregion
    # region Manual Execute
    eq_wrappers.manual_execution(base_request, qty, price)
    # endregion

    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion

    # region Book Order
    eq_wrappers.book_order(base_request, client, price, selected_row_count=2)
    # endregion
    # region Verify
    params = {
        'Account': '*',
        'Quantity': int(qty)*2,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': [
            {'PartyRole': "1",
             'PartyID': "ExecutingFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
            {'PartyRole': "28",
             'PartyRoleQualifier': "24",
             'PartyID': "Custodian - User",
             'PartyIDSource': "N"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"}
        ],
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'LastMkt': '*',
        'GrossTradeAmt': '*',
        'QuodTradeQualifier': '*',
        'NoOrders': [
            {'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
             'OrderID': '*'},
            {'ClOrdID': eq_wrappers.get_cl_order_id(base_request),
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'AllocType': '*',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',

    }
    fix_verifier_bo = FixVerifier(bo_connectivity, case_id)
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders'])
    # endregion
