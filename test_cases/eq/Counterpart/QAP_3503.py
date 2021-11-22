import logging
import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3503"
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_COUNTERPART"
    client2 = "CLIENT_COUNTERPART2"
    account = "CLIENT_COUNTERPART_SA1"
    account2 = "CLIENT_COUNTERPART2_SA1"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    bo_connectivity = test_framework.old_wrappers.eq_fix_wrappers.get_bo_connectivity()
    no_allocs = [
        {
            'AllocAccount': account,
            'AllocQty': qty
        }
    ]
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # region Create order via FIX
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)#,no_allocs
    response = fix_message.pop('response')
    eq_wrappers.accept_order('VETO', qty, price)
    # endregion
    # region Verify
    params = {
        'ExecType': '0',
        'OrdStatus': '0',
        'Side': 1,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'Currency': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'ExecBroker': '*',
        'NoParty': [
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "7",
             'PartyID': "InvestmentFirm - ClCounterpart_SA1",
             'PartyIDSource': "C"},
            {'PartyRole': "36",
             'PartyID': "gtwquod5",
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
                                         key_parameters=None)
    # endregion
    # region Manual Execute
    eq_wrappers.manual_execution(base_request, qty, price)
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
        'OrderID': '*',
        'TransactTime': '*',
        'LastCapacity': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'SettlDate': '*',
        'SettlType': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'Currency': '*',
        'VenueType': '*',
        'HandlInst': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'LastMkt': '*',
        'ExecBroker': '*',
        'NoParty': [
            {'PartyRole': "1",
             'PartyID': "ExecutingFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "7",
             'PartyID': "InvestmentFirm - ClCounterpart_SA1",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyRoleQualifier': "24",
             'PartyID': "TestExtIDClient",
             'PartyIDSource': "N"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "36",
             'PartyID': username,
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
    fix_verifier_bo.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType'])
    # endregion
    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region Book Order
    eq_wrappers.book_order(base_request, client2, price)
    # endregion
    # region Verify
    params = {
        'Quantity': qty,
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
            {'PartyRole': "22",
             'PartyID': "Exchange - ClCountepart2",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
            {'PartyRole': "28",
             'PartyRoleQualifier': "24",
             'PartyID': "TestExtIDClient",
             'PartyIDSource': "N"},
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
    param = [{"Security Account": account2, "Alloc Qty": qty}
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
            {'PartyRole': "1",
             'PartyID': "ExecutingFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "22",
             'PartyID': "Exchange - ClCountepart2",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
            {'PartyRole': "28",
             'PartyRoleQualifier': "24",
             'PartyID': "TestExtIDClient",
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
        'Quantity': qty,
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
            {'PartyRole': "22",
             'PartyID': "Exchange - ClCountepart2",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"},
            {'PartyRole': "28",
             'PartyRoleQualifier': "24",
             'PartyID': "TestExtIDClient",
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
                'AllocAccount': account2,
                'AllocPrice': price,
                'AllocQty': qty,

            }
        ],
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
