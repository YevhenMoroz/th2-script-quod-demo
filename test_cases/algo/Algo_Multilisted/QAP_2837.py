import os
import logging
from copy import deepcopy
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, ExtractionAction, CancelOrderDetails
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps, create_event, message_to_grpc, convert_to_request
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from test_framework.old_wrappers.fix_verifier import FixVerifier
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager
from custom.verifier import Verifier
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
import test_framework.old_wrappers.eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

qty = 1300
dec_qty = 1000
display_qty = 1100
price = 20
lookup = "PAR"       #CH0012268360_CHF
ex_destination = "XPAR"
account = 'XPAR_CLIENT2'
client = 'CLIENT2'
order_type = 2
ex_destination_1 = "XPAR"
report_id = None
extraction_id = "getOrderAnalysisAlgoParameters"
s_par = '1015'
s_trqx = '3416'
side = 1
instrument = {
            'Symbol': 'FR0000121121_EUR',
            'SecurityID': 'FR0000121121',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
tif_day = 0
currency = 'EUR'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_rule, ocrr_rule,ocr_rule]

def rule_destroyer(list_rules):
    rule_manager = RuleManager()
    for rule in list_rules:
        rule_manager.remove_rule(rule)


def send_market_data(symbol: str, case_id :str, market_data ):
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


def send_market_dataT(symbol: str, case_id :str, market_data ):
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

def order(ex_id, base_request, case_id):
    caseid = bca.create_event('Send order via FIX', case_id)
    # Send_MarkerData
    fix_manager_310 = FixManager(connectivity_sell_side, caseid)
    fix_verifier_ss = FixVerifier(connectivity_sell_side, caseid)
    fix_verifier_bs = FixVerifier(connectivity_buy_side, caseid)

    case_id_0 = bca.create_event("Send Market Data", caseid)
    market_data1 = [
        {
            'MDEntryType': '0',
            'MDEntryPx': '30',
            'MDEntrySize': '100000',
            'MDEntryPositionNo': '1'
        },
        {
            'MDEntryType': '1',
            'MDEntryPx': '40',
            'MDEntrySize': '100000',
            'MDEntryPositionNo': '1'
        }
    ]
    send_market_data(s_par, case_id_0, market_data1)
    market_data2 = [
        {
            'MDEntryType': '0',
            'MDEntryPx': '30',
            'MDEntrySize': '100000',
            'MDEntryPositionNo': '1'
        },
        {
            'MDEntryType': '1',
            'MDEntryPx': '40',
            'MDEntrySize': '100000',
            'MDEntryPositionNo': '1'
        }
    ]
    send_market_data(s_trqx, case_id_0, market_data2)

    case_id_1 = bca.create_event("Create Algo Order", caseid)
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
            'TargetStrategy': "1008",
            "DisplayInstruction":{
                'DisplayQty' : dec_qty
            },
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
    fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)
    fix_message_new_order_single.get_ClOrdID()
    
    time.sleep(2)

    #region Modify order
    case_id_3 = bca.create_event("Modify Order", case_id)
    fix_modify_message = deepcopy(fix_message_new_order_single)
    fix_modify_message.change_parameters({'DisplayInstruction': {'DisplayQty': display_qty}})
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    fix_manager_310.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id_3)

    act_ob = Stubs.win_act_order_book
    act = Stubs.win_act
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    call(act_ob.getOrdersDetails, ob.request())
    ob_qty = ExtractionDetail("orderbook.qty", "Qty")
    ob_limit_price = ExtractionDetail("orderbook.lmtprice", "Limit Price")
    ob_displ_qty = ExtractionDetail("orderbook.displQty", "DisplQty")
    ob_id = ExtractionDetail("orderBook.orderid", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")

    sub_order_qty = ExtractionDetail("subOrder_lvl_2.id", "Qty")
    sub_order_price = ExtractionDetail("subOrder_lvl_2.lmtprice", "Limit Price")
    sub_order_displ_qty = ExtractionDetail("subOrder_lvl_2.displQty", "DisplQty")
    sub_order_status = ExtractionDetail("subOrder_lvl_2.status", "Sts")
    sub_order_order_id = ExtractionDetail("subOrder_lvl_2.orderid", "Order ID")
    lvl2_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[sub_order_status,
                                                                                                      sub_order_qty,
                                                                                                      sub_order_price,
                                                                                                      sub_order_displ_qty,
                                                                                                      sub_order_order_id]))
    lvl2_details = OrdersDetails.create(info=lvl2_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_qty,
                                                                                 ob_id,
                                                                                 ob_limit_price,
                                                                                 ob_displ_qty,
                                                                                 ob_sts]),
            sub_order_details=lvl2_details))

    response = call(act_ob.getOrdersDetails, ob.request())

    order_id = response[ob_id.name]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check algo order")
    verifier.compare_values('Qty', str(qty), response[ob_qty.name].replace(",", ""))
    verifier.compare_values('Sts', 'Open', response[ob_sts.name])
    verifier.compare_values('LmtPrice', str(price), response[ob_limit_price.name])
    verifier.compare_values('DisplQty', str(display_qty), response[ob_displ_qty.name].replace(",", ""))
    verifier.verify()

    verifier.set_event_name("Check child order")
    verifier.compare_values('Qty', str(qty), response[sub_order_qty.name].replace(",", ""))
    verifier.compare_values('Sts', 'Cancelled', response[sub_order_status.name])
    verifier.compare_values('LmtPrice', str(price), response[sub_order_price.name])
    verifier.compare_values('DisplQty', str(display_qty), response[sub_order_displ_qty.name].replace(",", ""))
    verifier.verify()

    extraction_id = "getOrderAnalysisEvents"

    call(act.getOrderAnalysisEvents,
             create_order_analysis_events_request(extraction_id, {"Order ID": order_id}))


    vr = create_verification_request("checking order events", extraction_id, extraction_id)
    check_value(vr, "Event 1 Description contains", "event1.desc", "New User's Synthetic Order Received",
                    VerificationDetails.VerificationMethod.CONTAINS)

    check_value(vr, "Events Count", "events.count", "5")
    call(act.verifyEntities, vr)


    #region Cancel order
    case_id_4 = bca.create_event("Cancel Order", case_id)
    # Cancel order
    cancel_parms = {
        "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
        "Account": fix_message_new_order_single.get_parameter('Account'),
        "Side": fix_message_new_order_single.get_parameter('Side'),
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
    }
        
    fix_cancel = FixMessage(cancel_parms)
    fix_manager_310.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_4)


def execute(report_id, session_id):
    try:
        case_id = create_event(case_name, report_id)
        set_base(session_id, case_id)
        base_request = get_base_request(session_id, case_id)
        rule_list = rule_creation()
        order("getOrderInfo", base_request, case_id)
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)