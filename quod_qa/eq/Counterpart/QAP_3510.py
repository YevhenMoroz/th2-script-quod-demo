import logging
import time
from custom.basic_custom_actions import create_event
from quod_qa.wrapper.fix_verifier import FixVerifier
from quod_qa.wrapper_test.DataSet import Connectivity, Instrument
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3510"
    # region Declarations
    qty = {"OrderQty": "900"}
    price = "40"
    client = "CLIENT_COUNTERPART"
    account = "CLIENT_COUNTERPART_SA1"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    no_allocs = {"NoAllocs": [{'AllocAccount': account, 'AllocQty': qty["OrderQty"]}]}

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # ord_book = OMSOrderBook(case_id, session_id)
    # mo = OMSMiddleOfficeBook(case_id, session_id)
    # endregion
    # region Open FE
    # ord_book.open_fe(session_id, report_id, work_dir, username, password)
    # # endregion
    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
            Connectivity.Ganymede_317_bs.value, client + '_EUREX', 'XEUR', float(price))
        nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(Connectivity.Ganymede_317_bs.value,
                                                                                  client + '_EUREX', 'XEUR',
                                                                                  float(price),
                                                                                  traded_qty=int(qty["OrderQty"]),
                                                                                  delay=0)
        fix_message = FixMessageNewOrderSingleOMS()
        fix_message.set_default_DMA(Instrument.ISI1)
        fix_message.add_ClordId('QAP_3510')
        fix_message.change_parameters(dict(Account=client, OrderQtyData=qty, Price=price, PreAllocGrp=no_allocs))

        fix_manager = FixManager(Connectivity.Ganymede_317_ss.value, case_id)
        response = fix_manager.send_message_and_receive_response(fix_message)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule1)
        rule_manager.remove_rule(nos_rule)
    params = {
        'Account': client,
        'OrderQtyData': {'OrderQty': qty["OrderQty"]},
        'ReplyReceivedTime': '*',
        'ExecType': '0',
        'OrdStatus': '0',
        'Side': 1,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['ClOrdID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': '*',
        'TransactTime': '*',
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
        'Parties': {'NoPartyIDs': [
            {'PartyRole': "28",
             'PartyID': "CustodianUser",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "38",
             'PartyID': "PositionAccount - DMA Washbook",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "InvestmentFirm - ClCounterpart_SA1",
             'PartyIDSource': "C"}
        ]},
        'Instrument': '*',
        'SecondaryOrderID': '*',
        'Text': '*',
        'Price': price,

    }

    fix_verifier = FixVerifier(Connectivity.Ganymede_317_ss.value, case_id)
    fix_verifier.CheckExecutionReport(params, response, case=case_id,
                                      key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
    params = {
        'Account': client + "_EUREX",
        'OrderQtyData': {'OrderQty': qty["OrderQty"]},
        'ExecType': 'F',
        'OrdStatus': '2',
        'Side': 1,
        'TimeInForce': 0,
        'ClOrdID': response.response_messages_list[0].fields['OrderID'].simple_value,
        'ExecID': '*',
        'LastQty': '*',
        'OrderID': response.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'ExpireDate': '*',
        'AvgPx': '*',
        'SettlType': '*',
        'ExDestination': '*',
        'GrossTradeAmt': '*',
        'Currency': '*',
        'VenueType': '*',
        'LeavesQty': '*',
        'CumQty': '*',
        'LastPx': '*',
        'OrdType': '*',
        'OrderCapacity': '*',
        'QtyType': '*',
        'ExecBroker': '*',

        'Instrument': '*',
        'Price': price,
    }
    fix_verifier = FixVerifier(Connectivity.Ganymede_317_bs.value, case_id)
    fix_verifier.CheckExecutionReport(params, response, case=case_id,
                                      key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'], direction="SECOND")
    # mo.book_order()

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
    fix_verifier = FixVerifier(Connectivity.Ganymede_317_bo.value, case_id)
    fix_verifier.CheckAllocationInstruction(params, response, case=case_id,
                                            key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
    # mo.approve_block()
    # endregion
    # region Allocate
    # mo.allocate_block()
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
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirma",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyID': "CustodianUser",
             'PartyIDSource': "C"},
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
    fix_verifier.CheckConfirmation(params, response, case=case_id,
                                   key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])
    params = {
        'Quantity': qty,
        'TradeDate': '*',
        'TransactTime': '*',
        'AvgPx': '*',
        'Side': '*',
        'Currency': '*',
        'NoParty': [
            {'PartyRole': "67",
             'PartyID': "InvestmentFirm - ClCounterpart",
             'PartyIDSource': "C"},
            {'PartyRole': "66",
             'PartyID': "MarketMaker - TH2Route",
             'PartyIDSource': "C"},
            {'PartyRole': "17",
             'PartyID': "ContraFirma",
             'PartyIDSource': "C"},
            {'PartyRole': "28",
             'PartyID': "CustodianUser",
             'PartyIDSource': "C"},
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
    fix_verifier.CheckAllocationInstruction(params, response, ['NoOrders', 'AllocType'])
    # endregion
