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
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from rule_management import RuleManager
from custom.verifier import Verifier

logger = getLogger(__name__)
logger.setLevel(INFO)
qty = 2000
limit = 20
lookup = "CH0012268360_CHF"
ex_destination = "XPAR"
client = "CLIENT2"
order_type = "Limit"
case_name = os.path.basename(__file__)
report_id = None


def create_order(base_request):
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(str(qty))
    order_ticket.set_limit(str(limit))
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)

    participation_alog = order_ticket.add_quod_participation_strategy("Quod Participation")
    participation_alog.set_start_date("Now")
    participation_alog.set_end_date("Now", "0.2")
    participation_alog.set_aggressivity("Neutral")
    participation_alog.set_percentage_volume("30")

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)


    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())

def rule_creation(limit, client, ex_destination):
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-" + ex_destination.lower(), ex_destination + "_" + client, ex_destination, limit)
    ocr_rule = rule_manager.add_OrderCancelRequest('fix-bs-eq-'+ ex_destination.lower(), ex_destination + '_' + client, ex_destination, True)
    return [nos_rule, ocr_rule]

def rule_destroyer(list_rules):
    rule_manager = RuleManager()
    for rule in list_rules:
        rule_manager.remove_rule(rule)

def prepared_fe(case_id):
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id, work_dir)
    return  base_request

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
    verifier.compare_values('LmtPrice', str(limit), response[ob_limit_price.name])
    verifier.verify()

    extraction_id = "getOrderAnalysisAlgoParameters"

    call(act.getOrderAnalysisAlgoParameters,
         order_analysis_algo_parameters_request(extraction_id, ["Aggressivity"], {"Order ID": response[ob_id.name]}))

    call(act.verifyEntities, verification(extraction_id, "Checking algo parameters",
                                                 [verify_ent("Aggressivity", "Aggressivity", '2')]))


def execute(reportid):
    report_id = reportid
    case_id = create_event(case_name, report_id)
    base_request = prepared_fe(case_id)
    rule_list = rule_creation(limit, client, ex_destination)
    create_order(base_request)
    rule_destroyer(rule_list)
    check_order_book("check child", base_request, case_id)

