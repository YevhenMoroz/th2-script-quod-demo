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

qty = 200
side = 1
price = 40
ex_destination_1 = "XPAR"
client = "CLIENT3"
order_type = 4
account = 'XPAR_CLIENT3'
currency = 'EUR'
tif_day = 0

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'

instrument = {
    'Symbol': 'FR0000032302_EUR',
    'SecurityID': 'FR0000032302',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XPAR'
}
symbol = "944"


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
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-310-columbia", account, ex_destination_1, 40)
    ocr_rule = rule_manager.add_OrderCancelRequest("fix-bs-310-columbia", account, ex_destination_1, False)
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
        now = datetime.today() - timedelta(hours=3)
        case_id = bca.create_event(os.path.basename(__file__), report_id)

        fix_manager_310 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)


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
            'TargetStrategy': 1001,
            'ExDestination': 'XPAR',
            'StopPx': 35
        }
        fix_message_new_order_single = FixMessage(new_order_single_params)
        fix_message_new_order_single.add_random_ClOrdID()
        responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single,
                                                                                   case=case_id_1)

        mdir_params_incremental = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '40',
                'MDEntrySize': '100',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]

        send_incremental(symbol, case_id_0, mdir_params_incremental)
        send_incremental(symbol, case_id_0, mdir_params_incremental)

        cancel_parms = {
            "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
            "Account": fix_message_new_order_single.get_parameter('Account'),
            "Side": fix_message_new_order_single.get_parameter('Side'),
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
        }

        fix_cancel = FixMessage(cancel_parms)
        responce_cancel = fix_manager_310.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_0)


    except:
        logging.error("Error execution", exc_info=True)
    finally:
        time.sleep(5)
        rule_destroyer(rule_list)
