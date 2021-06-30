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
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager
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
before_order_details_id = "beforeTWAPAlgo_order_details"
after_order_details_id = "afterTWAPAlgo_order_details"
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
    now = datetime.today() - timedelta(hours=3)
    
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
                    'StrategyParameterValue': (now + timedelta(minutes=4)).strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'Waves',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '10'
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
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(before_order_details_id)
    main_order_details.set_filter(["Owner", 'gtwquod5'])

    main_order_status = ExtractionDetail("order_status", "Sts")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status,
                                                                                                     main_order_id])
    main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

    request = call(act_ob.getOrdersDetails, main_order_details.request())
    call(act.verifyEntities, verification(before_order_details_id, "checking order",
                                                     [verify_ent("Order Status", main_order_status.name, "Open")]))

    order_id = request[main_order_id.name]
    if not order_id:
        raise Exception("Order id is not returned")

    time.sleep(300)

    sub_order1_qty = ExtractionDetail("subOrder1.qty", "Qty")
    sub_order2_qty = ExtractionDetail("subOrder2.qty", "Qty")
    sub_order3_qty = ExtractionDetail("subOrder3.qty", "Qty")
    sub_order4_qty = ExtractionDetail("subOrder4.qty", "Qty")

    sub_order_details = OrdersDetails()
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order1_qty)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order2_qty)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order3_qty)))
    sub_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_detail=sub_order4_qty)))
    length_name = "subOrders.length"
    sub_order_details.extract_length(length_name)

    main_order_info = OrderInfo.create(sub_order_details=sub_order_details)

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(after_order_details_id)
    main_order_details.set_filter(["Order ID", order_id])
    main_order_details.add_single_order_info(main_order_info)

    call(act_ob.getOrdersDetails, main_order_details.request())

    call(act.verifyEntities, verification(after_order_details_id, "checking child orders",
                                                     [verify_ent("Sub order 1 qty", sub_order1_qty.name, "50"),
                                                      verify_ent("Sub order 2 qty", sub_order2_qty.name, "50"),
                                                      verify_ent("Sub order 3 qty", sub_order3_qty.name, "100"),
                                                      verify_ent("Sub order 4 qty", sub_order4_qty.name, "200"),
                                                      verify_ent("Sub order count", length_name, "4")]))

    extraction_id = "getOrderAnalysisAlgoParameters"

    call(act.getOrderAnalysisAlgoParameters,
            order_analysis_algo_parameters_request(extraction_id, ["Waves"], {"Order ID": request["order_id"]}))
    time.sleep(20)
    call(act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                     [verify_ent("Waves", "Waves", "4")]))
def execute(reportid):
    try:
        report_id = reportid
        case_id = create_event(case_name, report_id)
        base_request = prepared_fe(case_id)
        rule_list = rule_creation()
        cl_ord = create_order(case_id)
        check_order_book("before_order_details", base_request, case_id, cl_ord)
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)