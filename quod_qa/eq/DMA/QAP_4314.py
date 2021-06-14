import logging

from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails


from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails

from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP_4314"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    qty = "1000"  # Setting values for all orders
    price = "1.2"
    client = "HAKKIM"
    lookup = "RELIANCE"
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
    order_ticket.set_order_type("Limit")
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price)
    order_ticket.set_client(client)
    order_ticket.buy()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)
    order_ticket_service = Stubs.win_act_order_ticket
    common_act = Stubs.win_act

    call(order_ticket_service.placeOrder, new_order_details.build())
    extraction_id = "order.dma"
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(extraction_id)
    main_order_details.set_filter(["Lookup", lookup])
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")
    order_client = ExtractionDetail("order_client", "Client")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_client
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Status", order_status.name, "Open"),
                                                  verify_ent("Client", order_client.name, client)
                                                  ]))
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
