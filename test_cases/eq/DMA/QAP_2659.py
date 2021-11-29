import logging
from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps

from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-2659"
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    time = datetime.utcnow().isoformat()
    lookup = "SGOA"
    SecurityID = "FR0000125007"
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT1")
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
    try:
        # region Create order via FIX
        connectivity = 'gtwquod5'
        fix_manager_qtwquod5 = FixManager(connectivity, case_id)
        fix_params = {
            'Account': "CLIENT1",
            'HandlInst': "2",
            'Side': "2",
            'OrderQty': qty,
            'TimeInForce': "0",
            'OrdType': 2,
            'Price': price,
            'TransactTime': time,
            'ExDestination': 'CHIX',
            'Instrument': {
                'Symbol': 'FR0000125007_EUR',
                'SecurityID': SecurityID,
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR',
            },
            'Currency': 'EUR',
            'SecurityExchange': 'XPAR',
        }

        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
        # endregion
        # region Buy create order via FE
        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(price)
        order_ticket.set_client("CLIENT1")
        order_ticket.set_order_type("Limit")
        order_ticket.set_tif("Day")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.s
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
        order_qty = ExtractionDetail("order_qty", "Qty")
        order_tif = ExtractionDetail("order_tif", "TIF")
        order_ordType = ExtractionDetail("oder_ordType", "OrdType")
        order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                                order_qty,
                                                                                                order_tif,
                                                                                                order_ordType
                                                                                                ])
        order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
        call(act.getOrdersDetails, order_details.request())
        call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                     [verify_ent("Order Status", order_status.name, "Eliminated"),
                                                      verify_ent("Qty", order_qty.name, qty),
                                                      verify_ent("TIF", order_tif.name, "Day"),
                                                      verify_ent("OrdType", order_ordType.name, "Market")]))
        # endregion
    except Exception:
        logger.error("Error execution", exc_info=True)
        rule_manager.remove_rule(nos_rule)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

