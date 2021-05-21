import logging
import os
from copy import deepcopy
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID, Message
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

qty = 2000
display_qty = 100
limit = 20
side = 1
client = "KEPLER"
order_type = "Limit"
case_name = os.path.basename(__file__)
connectivity_fh = "fix-fh-310-columbia"
connectivity_bs = "fix-bs-310-columbia"
connectivity_ss = "fix-ss-310-columbia-standart"
listing_id1 = "9400000038"

instrument = {
            'Symbol': "FR0000125460_EUR",
            'SecurityID': "FR0000125460",
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-310-columbia-standard", "XPAR_" + client, "XPAR", limit)
    # ocr_rule = rule_manager.add_OrderCancelRequest('fix-bs-eq-' + ex_destination_1.lower(), ex_destination_1 + '_' + client, ex_destination_1, True)
    ocrr_rule = rule_manager.add_OCRR("fix-bs-eq-paris")
    return [nos_rule, ocrr_rule]

def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)

def send_MD(symbol: str, case_id :str):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
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
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_fh)
    ))

def execute(report_id):
    case_id = bca.create_event(os.path.basename(__file__), report_id)
    rule_list = rule_creation()

    fix_manager_ss = FixManager(connectivity_ss, case_id)
    fix_verifier_ss = FixVerifier(connectivity_ss, case_id)
    fix_verifier_bs = FixVerifier(connectivity_bs, case_id)


    # Send NewOrderSingle
    new_order_single_params = {
        'Account': client,
        'HandlInst': "2",
        'Side': side,
        'OrderQty': qty,
        'TimeInForce': "0",
        'Price': "20",
        'OrdType': "2",
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

    fix_message_new_order_single = FixMessage(new_order_single_params)
    fix_message_new_order_single.add_random_ClOrdID()
    responce_new_order_single = fix_manager_ss.Send_NewOrderSingle_FixMessage(fix_message_new_order_single)

    # #Check on ss
    # er_params_pending ={
    #     'ExecType': "A",
    #     'OrdStatus': 'A',
    #     'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
    # }
    # fix_verifier_ss.CheckExecutionReport(er_params_pending, responce_new_order_single)
    #
    # #Check on ss
    # er_params_new ={
    #     'ExecType': "0",
    #     'OrdStatus': '0',
    #     'OrderID': responce_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
    # }
    # fix_verifier_ss.CheckExecutionReport(er_params_new, responce_new_order_single)
    #
    # #Check on bs
    # new_order_single_bs = {
    #     'Side': new_order_single_params['Side'],
    #     'Price': new_order_single_params['Price']
    # }
    # fix_verifier_bs.CheckNewOrderSingle(new_order_single_bs, responce_new_order_single)





    rule_destroyer(rule_list)

