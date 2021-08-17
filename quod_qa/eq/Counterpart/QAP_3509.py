import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    global rule_manager, trade_rule, nos_rule1, fix_message
    case_name = "QAP-3509"
    # region Declarations
    qty = "800"
    price = "40"
    client = "CLIENT_COUNTERPART"
    account = "CLIENT_COUNTERPART_SA1"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    bo_connectivity = eq_wrappers.get_bo_connectivity()
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
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + '_PARIS', 'XPAR', float(price))
        nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                      client + '_PARIS', 'XPAR', float(price),
                                                                      traded_qty=int(qty), delay=0)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price, no_allocs)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(5)
        rule_manager.remove_rule(nos_rule1)
        rule_manager.remove_rule(nos_rule)

    response = fix_message.pop('response')
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
            {'PartyRole': "32",
             'PartyID': "Custodian - User2",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart_SA1",
             'PartyIDSource': "C"},
            {'PartyRole': "38",
             'PartyID': "PositionAccount - DMA Washbook",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "36",
             'PartyID': "gtwquod1",
             'PartyIDSource': "D"}
        ],
        'Instrument': '*',
        'SecondaryOrderID': '*',
        'LastMkt': '*',
        'Text': '*',
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
        'ExecBroker': '*',
        'NoParty': [
            {'PartyRole': "32",
             'PartyID': "Beneficiary",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirma",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyID': "Custodian",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody",
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
    fix_verifier_bo.CheckExecutionReport(params, response, message_name='Check params',
                                         key_parameters=['ClOrdID', 'ExecType', 'OrdStatus'])

    eq_wrappers.book_order(base_request, client, price)

    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': [
            {'PartyRole': "32",
             'PartyID': "Beneficiary",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyID': "Custodian",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"}
        ],
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
        'RootSettlCurrAmt': '*',
        'AllocTransType': '0',
        'ReportedPx': '*',
        'RootCommTypeClCommBasis': '*'

    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, None)

    eq_wrappers.approve_block(base_request)
    # endregion
    # region Allocate
    modify_request = ModifyTicketDetails(base_request)
    try:
        call(Stubs.win_act_middle_office_service.allocateMiddleOfficeTicket, modify_request.build())
    except Exception:
        logger.error("Error execution", exc_info=True)
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
            {'PartyRole': "32",
             'PartyID': "Custodian - User2",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirma",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyID': "Custodian",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"}
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
            {'PartyRole': "32",
             'PartyID': "Custodian - User2",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "67",
             'PartyID': "ContraFirm",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyID': "Custodian",
             'PartyIDSource': "C"},
            {'PartyRole': "34",
             'PartyID': "RegulatoryBody - Venue(Paris)",
             'PartyIDSource': "C"},
            {'PartyRole': "10",
             'PartyID': "CREST",
             'PartyIDSource': "D"}
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
                'AllocPrice': '40',
                'AllocQty': qty,

            }
        ],
    }
    fix_verifier_bo.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
