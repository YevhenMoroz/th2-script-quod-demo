import os
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

qty = 1300
account = "CLIENT1"
time_in_force = 0
price = 35
stop_price = 35
side = 1
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_feed_handler = "fix-fh-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
symbol_paris = "734"
symbol_trqx = "3416"
ord_type = 4
instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", price)
    occr_rule = rule_manager.add_OCRR(connectivity_buy_side)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, "XPAR_CLIENT1", "XPAR", True)
    return [nos_rule, occr_rule, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    fix_manager = FixManager(connectivity_sell_side, case_id)
    fix_verifier_sell_side = FixVerifier(connectivity_sell_side, case_id)
    fix_verifier_buy_side = FixVerifier(connectivity_buy_side, case_id)

    list_rules = rule_creation()



    case_id_1 = bca.create_event("Algo creation", case_id)
    case_id_2 = bca.create_event("MarketData send", case_id)
    case_id_3 = bca.create_event("Check buy-side", case_id)
    case_id_4 = bca.create_event("Cancel order", case_id)

    # Send NewOrderSingle
    multilisting_params = {
        'Account': account,
        'HandlInst': "2",
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': time_in_force,
        'StopPx': stop_price,
        'Price': price,
        'OrdType': ord_type,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': "1008",
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'AvailableVenues',
                'StrategyParameterType': '13',
                'StrategyParameterValue': 'true'
            },
            {
                'StrategyParameterName': 'AllowMissingPrimary',
                'StrategyParameterType': '13',
                'StrategyParameterValue': 'true'
            }
        ]
    }

    fix_message_multilisting = FixMessage(multilisting_params)
    fix_message_multilisting.add_random_ClOrdID()
    responce = fix_manager.Send_NewOrderSingle_FixMessage(fix_message_multilisting, case=case_id_1)
    time.sleep(1)


    time.sleep(5)
    # Send MD

    MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="734",
        connection_id=ConnectionID(session_alias="fix-fh-310-columbia")
    )).MDRefID

    mdir_params_trade = {
        'MDReqID': MDRefID_1,
        'NoMDEntriesIR': [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '38.5',
                'MDEntrySize': '3000',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    }
    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_2,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
    ))
    time.sleep(10)
    mdir_params_trade = {
        'MDReqID': MDRefID_1,
        'NoMDEntriesIR': [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '38.5',
                'MDEntrySize': '3000',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    }
    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh', "fix-fh-310-columbia", case_id_2,
        message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-fh-310-columbia")
    ))







    time.sleep(5)
    rule_destroyer(list_rules)