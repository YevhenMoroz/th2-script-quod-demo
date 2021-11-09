import os
import logging
import time
from datetime import datetime, timedelta
from copy import deepcopy
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from quod_qa.eq import MD_test
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 300
side = 1
price = 20
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
currency = 'EUR'
tif_day = 0

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-sell-side-316-ganymede"
connectivity_fh = 'fix-feed-handler-316-ganymede'

instrument = {
    'Symbol': 'FR0000061137_EUR',
    'SecurityID': 'FR0000061137',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XPAR'
}

symbol = "591"


def send_market_data(symbol: str, case_id: str, market_data):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_fh)
    ))


def send_incremental(symbol: str, case_id: str, market_data):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntriesIR': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataIncrementalRefresh', md_params, connectivity_fh)
    ))

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-buy-side-316-ganymede", account, ex_destination_1, 19.97)
    ocr_rule = rule_manager.add_OrderCancelRequest("fix-buy-side-316-ganymede", account, ex_destination_1, False)
    rule_manager.print_active_rules()
    return [nos_rule, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)

def execute(report_id):
    try:
        rule_list = rule_creation()
        now = datetime.today() - timedelta(hours=2)
        case_id = bca.create_event(os.path.basename(__file__), report_id)

        fix_manager_310 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)

        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '10',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '20',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(symbol, case_id_0, market_data1)

        mdir_params_incremental = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '17',
                'MDEntrySize': '120',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]

        send_incremental(symbol, case_id_0, mdir_params_incremental)
        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        new_order_single_params = {
            'Account': client,
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif_day,
            'OrdType': order_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Price': price,
            'Currency': currency,
            'TargetStrategy': 1005,
            'ExDestination': 'XPAR',
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'StartDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'EndDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': (now + timedelta(minutes=3)).strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'Passive',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'PRM'
                },
                {
                    'StrategyParameterName': 'PassiveOffset',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '-1'
                },
                {
                    'StrategyParameterName': 'LimitPriceReference',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'PRM'
                },
                {
                    'StrategyParameterName': 'LimitPriceOffset',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '-6'
                },
                {
                    'StrategyParameterName': 'Waves',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '3'
                }
            ]
        }
        fix_message_new_order_single = FixMessage(new_order_single_params)
        fix_message_new_order_single.add_random_ClOrdID()
        responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single,
                                                                                   case=case_id_1)
        rule_destroyer(rule_list)
    except:
        logging.error("Error execution", exc_info=True)
