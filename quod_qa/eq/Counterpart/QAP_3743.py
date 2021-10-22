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
    case_name = "QAP-3743"
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_COUNTERPART"
    account = "CLIENT_COUNTERPART_SA1"
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
    # endregion
    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            int(price), int(qty), 1)
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
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
        'Account': client,
        'ExecType': 'F',
        'OrdStatus': '2',
        'Side': 1,
        'TradeDate': '*',
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'SecondaryOrderID': '*',
        'Text': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'LastExecutionPolicy': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'SecondaryExecID': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'LastMkt': '*',
        'ExecBroker': '*',
        'NoParty': [
            {'PartyRole': "38",
             'PartyID': "PositionAccount - DMA Washbook",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "36",
             'PartyID': 'gtwquod1',
             'PartyIDSource': "D"}
        ],
        'Instrument': '*',
        'QuodTradeQualifier': '*',
        'BookID': '*',
        'Price': price,
        'OrderQtyData': {
            'OrderQty': qty
        }
    }
    fix_verifier_bo = FixVerifier(bo_connectivity, case_id)
    fix_verifier_bo.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
    # endregion
    # region Book Order
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    # region Verify
    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': [
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"}
        ],
        'Instrument': '*',
        'header': '*',
        'SettlDate': '*',
        'BookID': '*',
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
        'AllocType': '*',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',

    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, None)
    # endregion
    # region Approve
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Allocate
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
        'AllocAccount': '*',
        'ConfirmType': 2,
        'Side': '*',
        'Currency': '*',
        'BookID': '*',
        'NoParty': [
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart_SA1",
             'PartyIDSource': "C"}
        ],
        'Instrument': '*',
        'header': '*',
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
        'ConfirmTransType': '*',
        'ConfirmID': '*'
    }
    fix_verifier_bo.CheckConfirmation(params, response, None)
    params = {
        'Account': client,
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': [
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
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
             'OrderID': '*'}
        ],
        'AllocID': '*',
        'NetMoney': '*',
        'BookingType': '*',
        'AllocType': '2',
        'BookID': '*',
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'NoAllocs': [
            {
                'AllocNetPrice': '*',
                'AllocAccount': account,
                'AllocPrice': price,
                'AllocQty': qty,

            }
        ],
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
