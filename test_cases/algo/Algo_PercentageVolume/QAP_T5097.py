import os

from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, \
    ExtractionDetail, ExtractionAction
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
import time
from datetime import datetime
from stubs import Stubs
from logging import getLogger, INFO
from custom.basic_custom_actions import timestamps, create_event, message_to_grpc, convert_to_request
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager
from custom.verifier import Verifier

logger = getLogger(__name__)
logger.setLevel(INFO)
qty = 2000
price = 20
lookup = "PAR"       #CH0012268360_CHF
ex_destination = "XPAR"
account = 'XPAR_CLIENT2'
client = 'CLIENT2'
order_type = 2
ex_destination_1 = "XPAR"
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


def create_order(base_request):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(str(qty))
    order_ticket.set_limit(str(price))
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)

    participation_alog = order_ticket.add_quod_participation_strategy("Quod Participation")
    participation_alog.set_start_date("Now")
    participation_alog.set_end_date("Now", "0.2")
    participation_alog.set_aggressivity("Passive")
    participation_alog.set_percentage_volume("30")

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)


    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account,ex_destination_1, True)
    return [nos_rule, ocr_rule]

def rule_destroyer(list_rules):
    rule_manager = RuleManager()
    for rule in list_rules:
        rule_manager.remove_rule(rule)


def check_order_book(ex_id, base_request, case_id):
    act_ob = Stubs.win_act_order_book
    act = Stubs.win_act
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob_qty = ExtractionDetail("orderbook.qty", "Qty")
    ob_limit_price = ExtractionDetail("orderbook.lmtprice", "LmtPrice")
    ob_id = ExtractionDetail("orderBook.orderid", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")



    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_qty,
                                                                                 ob_id,
                                                                                 ob_limit_price,
                                                                                 ob_sts])))

    response = call(act_ob.getOrdersDetails, ob.request())




    verifier = Verifier(case_id)
    verifier.set_event_name("Check algo order")
    verifier.compare_values('Qty', str(qty), response[ob_qty.name].replace(",", ""))
    verifier.compare_values('Sts', 'Open', response[ob_sts.name])
    verifier.compare_values('LmtPrice', str(price), response[ob_limit_price.name])
    verifier.verify()

    extraction_id = "getOrderAnalysisAlgoParameters"

    call(act.getOrderAnalysisAlgoParameters,
         order_analysis_algo_parameters_request(extraction_id, ["Aggressivity"], {"Order ID": response[ob_id.name]}))

    call(act.verifyEntities, verification(extraction_id, "Checking algo parameters",
                                                 [verify_ent("Aggressivity", "Aggressivity", '1')]))


def execute(report_id, session_id):
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    rule_list = rule_creation()
    create_order(base_request)
    rule_destroyer(rule_list)
    check_order_book("check child", base_request, case_id)

