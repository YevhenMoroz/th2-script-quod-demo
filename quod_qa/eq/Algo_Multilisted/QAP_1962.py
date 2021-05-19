import os
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

qty = 2000
display_qty = 100
price = 33
side = 2
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_feed_handler = "fix-fh-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
symbol_paris = "734"
symbol_trqx = "3416"

def rule_creation():
    rule_manager = RuleManager()
    ioc_rule_1 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, "KEPLER", "QDD1", False, qty, price)
    ioc_rule_2 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, "KEPLER", "QDD2", False, qty, price)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "KEPLER", "QDL1", price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "KEPLER", "QDL1", True)
    return [nos_rule, ioc_rule_1, ioc_rule_2, ocr_rule]

def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)

def send_MD(symbol: str, case_id :str):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_feed_handler)
    )).MDRefID
    mdir_params_bid = {
        'MDReqID': MDRefID,
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '250',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
                'MDEntrySize': '500',
                'MDEntryPositionNo': '1'
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_feed_handler,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_feed_handler)
    ))




def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    # fix_manager = FixManager(connectivity_sell_side, case_id)
    # fix_verifier_sell_side = FixVerifier(connectivity_sell_side, case_id)
    # fix_verifier_buy_side = FixVerifier(connectivity_buy_side, case_id)
    #
    # case_id_1 = bca.create_event("Algo creation", case_id)
    #
    # # Send NewOrderSingle
    # multilisting_params = {
    #     'Account': "CLIENT1",
    #     'HandlInst': "2",
    #     'Side': "1",
    #     'OrderQty': "1300",
    #     'TimeInForce': "0",
    #     'StopPx': "20",
    #     'OrdType': "3",
    #     'TransactTime': datetime.utcnow().isoformat(),
    #     'Instrument': {
    #         'Symbol': 'FR0000121121_EUR',
    #         'SecurityID': 'FR0000121121',
    #         'SecurityIDSource': '4',
    #         'SecurityExchange': 'XPAR'
    #     },
    #     'OrderCapacity': 'A',
    #     'Currency': 'EUR',
    #     'TargetStrategy': "1008",
    #     'NoStrategyParameters': [
    #         {
    #             'StrategyParameterName': 'AvailableVenues',
    #             'StrategyParameterType': '13',
    #             'StrategyParameterValue': 'true'
    #         },
    #         {
    #             'StrategyParameterName': 'AllowMissingPrimary',
    #             'StrategyParameterType': '13',
    #             'StrategyParameterValue': 'true'
    #         }
    #     ]
    # }
    #
    # fix_message_multilisting = FixMessage(multilisting_params)
    # fix_message_multilisting.add_random_ClOrdID()
    # responce = fix_manager.Send_NewOrderSingle_FixMessage(fix_message_multilisting, case=case_id_1)


    send_MD(case_id, symbol_trqx)


