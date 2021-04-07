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


logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = os.path.basename(__file__)

    # Create sub-report for case
    case_id = create_event(case_name, report_id)



    qty = "2000"
    limit = 20
    lookup = "BRNL"
    ex_destination = "XPAR"
    client = "CLIENT2"


    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris", ex_destination +"_"+ client, ex_destination, limit)
    ocr_rule = rule_manager.add_OrderCancelRequest('fix-bs-eq-paris','XPAR_CLIENT2','XPAR', True)

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


    try:
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(str(limit))
        order_ticket.set_client(client)
        order_ticket.set_order_type("Limit")

        twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
        twap_strategy.set_start_date("Now")
        twap_strategy.set_end_date("Now", "0.2")
        twap_strategy.set_aggressivity("Passive")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)




        set_base(session_id, case_id)

        order_ticket_service = Stubs.win_act_order_ticket


        call(order_ticket_service.placeOrder, new_order_details.build())


    except Exception:
        logger.error("Error execution", exc_info=True)
    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
    # close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
