import logging
import os
from datetime import datetime
from time import sleep

from win_gui_modules.application_wrappers import FEDetailsRequest
from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request, fields_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-1025"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT1"
    time = datetime.utcnow().isoformat()
    lookup = "PROL"
    # endregion

    # region Open FE

    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    username2 = Stubs.custom_config['qf_trading_fe_user2']
    password2 = Stubs.custom_config['qf_trading_fe_password2']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)

    # endregion

    # region switch to user2
    init_event = create_event("Initialization", parent_id=report_id)
    search_fe_req = FEDetailsRequest()
    search_fe_req.set_session_id(session_id)
    search_fe_req.set_parent_event_id(init_event)
    Stubs.moveToActiveFE(search_fe_req.build())
    # endregion

    # region Create CO
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT1")
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_limit(price)
    order_ticket.set_client(client)
    order_ticket.set_order_type("Limit")
    order_ticket.set_care_order(Stubs.custom_config['qf_trading_fe_user2'], True)

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    set_base(session_id, case_id)

    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act

    call(order_ticket_service.placeOrder, new_order_details.build())
    rule_manager.remove_rule(nos_rule)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    '''
    order_tif = ExtractionDetail("order_tif", "TIF")
    order_ordType = ExtractionDetail("oder_ordType", "OrdType")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                                order_qty,
                                                                                                order_price,
                                                                                                ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                     [verify_ent("Order Status", order_status.name, "Sent"),
                                                      verify_ent("Qty", order_qty.name, qty),
                                                      verify_ent("LmtPrice", order_price.name, price)
                                                      ]))
    '''
    # endregion

    # region Accept CO (not th2)
    # call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # Set shortcut for client inbox
    pyautogui.press("c")
    # Holds down the alt key
    pyautogui.keyDown("ctrl")
    # Presses the tab key once
    pyautogui.press("h")
    # Lets go of the alt key
    pyautogui.keyUp("ctrl")
    pyautogui.click()
    # endregion

    #close_fe(case_id, session_id)
    # region Check values in OrderBook after Accept
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                     [verify_ent("Order Status", order_status.name, "Open")]))
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
