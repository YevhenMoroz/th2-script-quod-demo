import logging
import os
from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from test_cases.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2547"
    seconds, nanos = timestamps()  # Store case start tim
    # region Declarations
    act = Stubs.win_act_order_book
    qty = "50"
    price = "2"
    client = "CLIENTYMOROZ"
    account = "YM_client_SA1"
    lookup = "VETO"
    capacity = "Agency"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # endregion

    # region Create order via FE
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price)
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.set_tif("Day")
    order_ticket.set_account(account)

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    call(order_ticket_service.placeOrder, new_order_details.build())
    extraction_id = "order.dma"
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(extraction_id)
    main_order_details.set_filter(["Lookup", lookup])

    call(order_book_service.getOrdersDetails, main_order_details.request())

    # endregion
    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_client = ExtractionDetail("order_client", "Client")
    order_account = ExtractionDetail("order_account", "Account ID")
    order_capacity = ExtractionDetail("order_capacity", "Capacity")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_client,
                                                                                            order_account,
                                                                                            order_capacity
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Status", order_status.name, "Open"),
                                                  verify_ent("Client", order_client.name, client),
                                                  verify_ent("Account ID", order_account.name, account),
                                                  verify_ent("Capacity", order_capacity.name, capacity)]))
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")