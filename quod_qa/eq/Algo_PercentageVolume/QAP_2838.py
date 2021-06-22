import os
import logging
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

qty = 2000
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
side = 2
instrument = {
            'Symbol': 'FR0010263202_EUR',
            'SecurityID': 'FR0010263202',
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
    caseid = bca.create_event('Send order via FIX', case_id)
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
            'Currency': currency,
            'TargetStrategy': 2,
                'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'PercentageVolume',
                    'StrategyParameterType': '11',
                    'StrategyParameterValue': '30'
                },
                {
                    'StrategyParameterName': 'Aggressivity',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '2'
                }
            ]
        }
    fix_message_new_order_single = FixMessage(new_order_single_params)
    fix_message_new_order_single.add_random_ClOrdID()
    fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)
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
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_rule, ocr_rule]

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
    call(act_ob.getOrdersDetails, ob.request())
    ob_qty = ExtractionDetail("orderbook.qty", "Qty")
    ob_limit_price = ExtractionDetail("orderbook.lmtprice", "LmtPrice")
    ob_id = ExtractionDetail("orderBook.orderid", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")

    sub_order_qty = ExtractionDetail("subOrder_lvl_2.id", "Qty")
    sub_order_price = ExtractionDetail("subOrder_lvl_2.lmtprice", "LmtPrice")
    sub_order_status = ExtractionDetail("subOrder_lvl_2.status", "Sts")
    sub_order_order_id = ExtractionDetail("subOrder_lvl_2.orderid", "Order ID")
    lvl2_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[sub_order_status,
                                                                                                      sub_order_qty,
                                                                                                      sub_order_price,
                                                                                                      sub_order_order_id]))
    lvl2_details = OrdersDetails.create(info=lvl2_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_qty,
                                                                                 ob_id,
                                                                                 ob_limit_price,
                                                                                 ob_sts]),
            sub_order_details=lvl2_details))

    response = call(act_ob.getOrdersDetails, ob.request())


    # print(ob_qty.name)
    # print(ob_id.name)
    # print(ob_limit_price.name)
    # print(sub_order_status.name)
    # print(sub_order_qty.name)
    # print(sub_order_price.name)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check algo order")
    verifier.compare_values('Qty', str(qty), response[ob_qty.name].replace(",", ""))
    verifier.compare_values('Sts', 'Open', response[ob_sts.name])
    verifier.compare_values('LmtPrice', str(price), response[ob_limit_price.name])
    verifier.verify()

    verifier.set_event_name("Check child order")
    verifier.compare_values('Qty', str(43), response[sub_order_qty.name].replace(",", ""))
    verifier.compare_values('Sts', 'Open', response[sub_order_status.name])
    verifier.compare_values('LmtPrice', str(price), response[sub_order_price.name])
    verifier.verify()


    call(act.getOrderAnalysisAlgoParameters,
         order_analysis_algo_parameters_request(extraction_id, ["Aggressivity", "PercentageVolume"], {"Order ID": response[ob_id.name]}))

    call(act.verifyEntities, verification(extraction_id, "Checking algo parameters",
                                                 [verify_ent("Aggressivity", "Aggressivity", '2')]))

    call(act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                     [verify_ent("PercentageVolume", "PercentageVolume", "30.0")]))


def execute(reportid):
    try:
        report_id = reportid
        case_id = create_event(case_name, report_id)
        base_request = prepared_fe(case_id)
        rule_list = rule_creation()
        cl_ord = create_order(case_id)
        check_order_book("Test_FE_id", base_request, case_id, cl_ord)
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)