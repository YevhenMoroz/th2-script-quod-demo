import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.order_book_wrappers import ManualExecutingDetails
from win_gui_modules.order_book_wrappers import CompleteOrdersDetails
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.wrappers import *
from rule_management import RuleManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    rule_manager = RuleManager()

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-3307"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    session_id = set_session_id()
    #set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:
        qty = "50"
        limit = "10"
        lookup = "VETO"

        # create care order
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)
        order_ticket.set_client("MOClient")
        order_ticket.set_order_type("Limit")
        order_ticket.set_care_order(Stubs.custom_config['qf_trading_fe_user_305'], True)

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)

        set_base(session_id, case_id)

        order_ticket_service = Stubs.win_act_order_ticket
        order_book_service = Stubs.win_act_order_book
        common_act = Stubs.win_act

        call(order_ticket_service.placeOrder, new_order_details.build())

        order_info_extraction = "getOrderInfo"

        data = call(common_act.getOrderFields, fields_request(order_info_extraction,
                                                             ["order.status", "Sts", "order.order_id", "Order ID"]))
        care_order_id = data["order.order_id"]
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order Status", "order.status", "Open")]))

        #create manual execution
        service = Stubs.win_act_order_book

        manual_executing_details = ManualExecutingDetails(base_request)
        manual_executing_details.set_filter({"Order ID": care_order_id})
        # manual_executing_details.set_row_number(1)

        executions_details = manual_executing_details.add_executions_details()
        executions_details.set_quantity(qty)
        executions_details.set_price(limit)
        executions_details.set_executing_firm("ExecutingFirm")
        executions_details.set_contra_firm("Contra_Firm")
        executions_details.set_last_capacity("Agency")

        call(service.manualExecution, manual_executing_details.build())

        #complete order
        service = Stubs.win_act_order_book

        complete_orders_details = CompleteOrdersDetails(base_request)
        complete_orders_details.set_filter({"Order ID": care_order_id})
        # complete_orders_details.set_selected_row_count(2)

        call(service.completeOrders, complete_orders_details.build())


        # book order
        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["Owner", username, "Order ID", care_order_id])
        #modify_request.set_selected_row_count(4)

        ticket_details = modify_request.add_ticket_details()
        ticket_details.set_client("MOClient")
        ticket_details.set_trade_date("2/21/2021")
        ticket_details.set_net_gross_ind("Gross")
        # ticket_details.set_give_up_broker("GiveUpBroker")
        ticket_details.set_agreed_price("5")

        settlement_details = modify_request.add_settlement_details()
        settlement_details.set_settlement_type("Regular")
        settlement_details.set_settlement_currency("EUR")
        settlement_details.set_exchange_rate("1")
        settlement_details.set_exchange_rate_calc("Multiply")
        # settlement_details.toggle_settlement_date()
        settlement_details.set_settlement_date("2/21/2021")
        settlement_details.toggle_recompute()

        commissions_details = modify_request.add_commissions_details()
        #commissions_details.toggle_manual()
        commissions_details.add_commission(basis="Absolute", rate="5")

        extraction_details = modify_request.add_extraction_details()
        extraction_details.set_extraction_id("BookExtractionId")
        extraction_details.extract_net_price("book.netPrice")
        extraction_details.extract_net_amount("book.netAmount")
        extraction_details.extract_total_comm("book.totalComm")
        extraction_details.extract_gross_amount("book.grossAmount")
        extraction_details.extract_total_fees("book.totalFees")
        extraction_details.extract_agreed_price("book.agreedPrice")

        response = call(middle_office_service.bookOrder, modify_request.build())

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
