import os
import logging
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, ExtractionAction, CancelOrderDetails
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime, timedelta
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps, create_event, message_to_grpc, convert_to_request
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
from custom.verifier import Verifier
import quod_qa.wrapper.eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

qty = 200
price = 1
lookup = "PAR"       #CH0012268360_CHF
ex_destination = "XPAR"
account = 'XPAR_CLIENT2'
client = 'CLIENT2'
order_type = 2
ex_destination_1 = "XPAR"
report_id = None
extraction_id = "getOrderAnalysisEvents"
s_par = '982'
side = 2
instrument = {
            'Symbol': 'FR0000044448_EUR',
            'SecurityID': 'FR0000044448',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
tif_day = 0
currency = 'EUR'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'


def create_order(case_id):
    now = datetime.today() - timedelta(hours=2)
    
    caseid = bca.create_event('Send Order via FIX', case_id)
        # Send_MarkerData
    fix_manager_310 = FixManager(connectivity_sell_side, caseid)
    fix_verifier_ss = FixVerifier(connectivity_sell_side, caseid)
    fix_verifier_bs = FixVerifier(connectivity_buy_side, caseid)

    case_id_0 = bca.create_event("Send Market Data", caseid)
    market_data2 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '20',
                'MDEntrySize': '100',
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
    send_market_dataT(s_par, case_id_0, market_data2)

    market_data3 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            }
        ]
    send_market_data(s_par, case_id_0, market_data3)

    #quod_qa.wrapper.eq_wrappers.create_order_via_fix()

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
            'ExDestination': ex_destination_1,
            'Currency': currency,
            'TargetStrategy': 1005,
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'StartDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'EndDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': (now + timedelta(minutes=5)).strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'SliceDuration',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '1'
                },                
                {
                    'StrategyParameterName': 'Aggressivity',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '3'
                }
            ]
        }
    fix_message_new_order_single = FixMessage(new_order_single_params)
    fix_message_new_order_single.add_random_ClOrdID()
    fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single,  case=case_id_1)
    cl_ord = fix_message_new_order_single.get_ClOrdID()
    return cl_ord


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


def rule_creation():
    rule_manager = RuleManager()
    nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, False, qty, price)
    return [nos_ioc_rule]

def rule_destroyer(list_rules):
    rule_manager = RuleManager()
    for rule in list_rules:
        rule_manager.remove_rule(rule)

def prepared_fe(case_id):
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id, work_dir)
    return  base_request

def check_order_book(ex_id, base_request, case_id, cl_ord):
    act_ob = Stubs.win_act_order_book
    act = Stubs.win_act
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob.set_filter(['ClOrdID', str(cl_ord)])

    ob_qty = ExtractionDetail("orderbook.qty", "Qty")
    ob_limit_price = ExtractionDetail("orderbook.lmtprice", "Limit Price")
    ob_id = ExtractionDetail("orderBook.orderid", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")


    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_qty,
                                                                                 ob_id,
                                                                                 ob_limit_price,
                                                                                 ob_sts])))

    call(act_ob.getOrdersDetails, ob.request())


    # region extraction Child order details
    child_order_info_extraction = "getOrderInfoChild"
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(child_order_info_extraction)

    child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
    child1_order_qty = ExtractionDetail("subOrder_lvl_1.Qty", "Qty")
    sub_lvl1_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child1_id, child1_order_qty])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action])

    child2_id = ExtractionDetail("subOrder_lvl_2.id", "Order ID")
    child2_order_qty = ExtractionDetail("subOrder_lvl_2.Qty", "Qty")
    sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child2_id, child2_order_qty])
    sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

    child3_id = ExtractionDetail("subOrder_lvl_3.id", "Order ID")
    child3_order_qty = ExtractionDetail("subOrder_lvl_3.Qty", "Qty")
    sub_lvl1_3_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child3_id, child3_order_qty])
    sub_lv1_3_info = OrderInfo.create(actions=[sub_lvl1_3_ext_action])

    child4_id = ExtractionDetail("subOrder_lvl_4.id", "Order ID")
    child4_order_qty = ExtractionDetail("subOrder_lvl_4.Qty", "Qty")
    sub_lvl1_4_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child4_id, child4_order_qty])
    sub_lv1_4_info = OrderInfo.create(actions=[sub_lvl1_4_ext_action])

    time.sleep(240)
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info,
                                                              sub_lv1_2_info,
                                                              sub_lv1_3_info,
                                                              sub_lv1_4_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_order_details))

    # child request
    call(act_ob.getOrdersDetails, child_main_order_details.request())
    # end region extraction

    # region verify Child details
    call(act.verifyEntities, verification(child_order_info_extraction, "checking Child order",
                                                 [verify_ent("Child Order Qty - 1", child1_order_qty.name, "50"),
                                                  verify_ent("Child Order Qty - 2", child2_order_qty.name, "50"),
                                                  verify_ent("Child Order Qty - 3", child3_order_qty.name, "100"),
                                                  verify_ent("Child Order Qty - 4", child4_order_qty.name, "200")]))
    # end region
    ob.set_filter(['ClOrdID', str(cl_ord)])
    response = call(act_ob.getOrdersDetails, ob.request())

    call(act.getOrderAnalysisEvents,
         create_order_analysis_events_request(extraction_id, {"Order ID": response[ob_id.name]}))
    

    vr = create_verification_request("checking order events", extraction_id, extraction_id)

    check_value(vr, "Event 1 Desc contains", "event1.desc", "To comply with quantity constraints, changing slice duration from 60 sec to ",
                    VerificationDetails.VerificationMethod.CONTAINS)
    
    call(act.verifyEntities, vr)

def execute(report_id, session_id):
    try:
        case_id = create_event(case_name, report_id)
        set_base(session_id, case_id)
        base_request = get_base_request(session_id, case_id)
        rule_list = rule_creation()
        cl_ord = create_order(case_id)
        check_order_book("before_order_details", base_request, case_id, cl_ord)  #getOrdersDetails
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)