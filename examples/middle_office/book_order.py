from datetime import datetime
from logging import getLogger, INFO

from custom.basic_custom_actions import timestamps, create_event
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call
from win_gui_modules.wrappers import *

logger = getLogger(__name__)
logger.setLevel(INFO)


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "Book order example"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)

    try:
        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["Owner", username, "Order ID", "MO"])
        # modify_request.set_selected_row_count(4)

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
        commissions_details.toggle_manual()
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
    except Exception:
        logger.error("Error execution", exc_info=True)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
