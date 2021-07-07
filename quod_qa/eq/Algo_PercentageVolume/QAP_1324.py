import os
import logging
import math
from custom import basic_custom_actions as bca
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, ExtractionAction, CancelOrderDetails
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
start_ltq = 200
oo_qty = 60  #open order
percentage = 30
ioc_qty = 40
ltq_child_qty = math.ceil((percentage * start_ltq) / (100 - percentage))
md_child_qty = math.ceil((percentage * oo_qty) / (100 - percentage))
MDEntrySize = 52
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
tif_ioc = 3
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

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination, price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination, True)
    nos_trade_by_qty_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination, price, price, 86, oo_qty, 0)
    nos_ioc_ltq_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination, False, 40, price)
    return [nos_rule, nos_trade_by_qty_rule, ocr_rule, nos_ioc_ltq_rule]

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

def order(base_request, case_id):
        ob_act = Stubs.win_act_order_book
        act = Stubs.win_act
        case_id_0 = bca.create_event("Send Market Data", case_id)

        market_data2 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '1',
                'MDEntrySize': start_ltq,
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
                'MDEntryPx': '1',
                'MDEntrySize': oo_qty,
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

        market_data4 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '1',
                'MDEntrySize': oo_qty,
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
        send_market_dataT(s_par, case_id_0, market_data4)

        market_data5 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '1',
                'MDEntrySize': '52',   
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data5)

        market_data15 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '52',   
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data15)

        time.sleep(3)

        order_info_extraction = "getOrderInfo"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        call(ob_act.getOrdersDetails, main_order_details.request())

        main_order_qty = ExtractionDetail("orderbook.qty", "Qty")
        main_order_lmt_price = ExtractionDetail("orderbook.lmtprice", "Limit Price")
        main_order_id = ExtractionDetail("orderBook.orderid", "Order ID")
        main_order_sts = ExtractionDetail("orderBook.sts", "Sts")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_qty, main_order_lmt_price, main_order_id, main_order_sts])
        
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        response = call(ob_act.getOrdersDetails, main_order_details.request())

        order_id = response[main_order_id.name]
        main_order_details.set_filter(['Order ID', order_id])
        call(ob_act.getOrdersDetails, main_order_details.request())

        order_amend = OrderTicketDetails()
        vol_stategy = order_amend.add_quod_participation_strategy('Quod Participation')
        vol_stategy.set_aggressivity('Aggressive')

        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_order_details(order_amend)
        call(Stubs.win_act_order_book.amendOrder, amend_order_details.build())

        
        case_id_1 = bca.create_event("Send Market Data", case_id)

        market_data6 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': '1',
                'MDEntrySize': oo_qty,
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
        send_market_dataT(s_par, case_id_1, market_data6)

        market_data7 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '1',
                'MDEntrySize': '26',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_1, market_data7)
        time.sleep(1)
        after_order_details_id = "afterParsitipationAlgo_order_details"     

        sub_order1_qty = ExtractionDetail("subOrder1.tif", "TIF")
    
        sub_order2_qty = ExtractionDetail("subOrder2.tif", "TIF")

        sub_order3_qty = ExtractionDetail("subOrder3.tif", "TIF")

        sub_order4_qty = ExtractionDetail("subOrder4.tif", "TIF")


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

        call(ob_act.getOrdersDetails, main_order_details.request())

        call(act.verifyEntities, verification(after_order_details_id, "checking child orders",
                                                     [verify_ent("Sub order 1 qty", sub_order1_qty.name, 'Day'),
                                                      verify_ent("Sub order 2 qty", sub_order2_qty.name, 'Day'),
                                                      verify_ent("Sub order 3 qty", sub_order3_qty.name, 'ImmediateOrCancel'),
                                                      verify_ent("Sub order 4 qty", sub_order4_qty.name, 'Day'),
                                                      verify_ent("Sub order count", length_name, "4")]))

        cancel_order_details = CancelOrderDetails()
        cancel_order_details.set_default_params(base_request)
        call(ob_act.cancelOrder, cancel_order_details.build())

def execute(report_id, session_id):
    try:
        case_id = create_event(case_name, report_id)
        set_base(session_id, case_id)
        base_request = get_base_request(session_id, case_id)
        rule_list = rule_creation()
        order(base_request, case_id)        
    except:
        logging.error("Error execution",exc_info=True)
    finally:
        rule_destroyer(rule_list)