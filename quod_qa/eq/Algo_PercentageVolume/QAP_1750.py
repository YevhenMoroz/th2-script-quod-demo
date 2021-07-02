import os
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, ExtractionAction
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom.basic_custom_actions import timestamps, create_event, message_to_grpc, convert_to_request
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager
from custom.verifier import Verifier

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

qty = 1000
child_qty_1 = 86
child_qty_2 = 43
child_qty_3 = 67
text_pn='Pending New status'
text_n='New status'
text_ocrr='OCRRRule'
text_c='order canceled'
text_f='Fill'
text_ret = 'reached end time'
text_s = 'sim work'
side = 1
price = 1
tif_day = 0
ex_destination = "XPAR"
client = "CLIENT2"
order_type = 'Limit'
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '1015'
lookup = 'PAR'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'

report_id = None


def create_order(base_request, case_id):
    case_id_0 = bca.create_event("Send Market Data", case_id)

    market_data2 = [
        {
            'MDUpdateAction': '0',
            'MDEntryType': '2',
            'MDEntryPx': '1',
            'MDEntrySize': '200',
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

    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(str(qty))
    order_ticket.set_limit(str(price))
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)

    vol_strategy = order_ticket.add_quod_participation_strategy("Quod Participation")
    #vol_strategy.set_start_date("Now")
    vol_strategy.set_percentage_volume('30')
    vol_strategy.set_aggressivity("Neutral")

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)


    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())

    case_id_0 = bca.create_event("Send Market Data", case_id)

    market_data3 = [
        {
            'MDEntryType': '0',
            'MDEntryPx': '1',
            'MDEntrySize': '186',
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

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination, price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination, True)
    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)
    return [nos_rule, ocr_rule, ocrr_rule]

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

def check_order_book(ex_id, base_request, case_id):
        time.sleep(3)
        ob_act = Stubs.win_act_order_book

        order_info_extraction = "getOrderInfo"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_id = ExtractionDetail("order_id", "Order ID")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_id])
        
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        main_order_response = call(ob_act.getOrdersDetails, main_order_details.request())


        order_amend = OrderTicketDetails()
        vol_stategy = order_amend.add_quod_participation_strategy('Quod Participation')
        vol_stategy.set_percentage_volume('40')

        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_order_details(order_amend)
        call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())

        
        case_id_1 = bca.create_event("Send Market Data", case_id)

        market_data4 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '1',
                'MDEntrySize': '143',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_1, market_data4)


        child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
        child1_qty = ExtractionDetail("subOrder_lvl_1.qty", "Qty")
        child1_sts = ExtractionDetail("subOrder_lvl_1.sts", "Sts")
        child1_price = ExtractionDetail("subOrder_lvl_1.lmtprice", "Limit Price")
        sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
            extraction_details=[child1_id, child1_qty, child1_sts, child1_price])
        sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])

        child2_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
        child2_qty = ExtractionDetail("subOrder_lvl_1.qty", "Qty")
        child2_sts = ExtractionDetail("subOrder_lvl_1.sts", "Sts")
        child2_price = ExtractionDetail("subOrder_lvl_1.lmtprice", "Limit Price")
        sub_lvl1_2_ext_action1 = ExtractionAction.create_extraction_action(
            extraction_details=[child2_id, child2_qty, child2_sts, child2_price])
        sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action1])

        sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info, sub_lv1_2_info])

        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
        child_response = call(ob_act.getOrdersDetails, main_order_details.request())

        verifier = Verifier(case_id)

        verifier.set_event_name("Check child order 1")
        verifier.compare_values('Qty', str(child_qty_1), child_response[child1_qty.name].replace(",", ""))
        verifier.compare_values('Sts', 'Open', child_response[child1_sts.name])
        verifier.compare_values('Limit Price', str(price), child_response[child1_price.name])
        verifier.verify()

        verifier.set_event_name("Check child order 2")
        verifier.compare_values('Qty', str(child_qty_2), child_response[child2_qty.name].replace(",", ""))
        verifier.compare_values('Sts', 'Open', child_response[child2_sts.name])
        verifier.compare_values('Limit Price', str(price), child_response[child2_price.name])
        verifier.verify()




def execute(reportid):
    try:
        report_id = reportid
        case_id = create_event(case_name, report_id)
        base_request = prepared_fe(case_id)
        rule_list = rule_creation()
        create_order(base_request, case_id)
        check_order_book("Test_FE_id", base_request, case_id)        
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)