import logging
import os
from copy import deepcopy
from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request, fields_request
import pyautogui

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-1021"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    qty2 = "400"
    price = "20"
    price2 = "50"
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

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # endregion
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-bs-eq-paris",
                                                                             "XPAR_" + client, "XPAR", 20)
        connectivity = 'gtwquod5'
        fix_manager_qtwquod5 = FixManager(connectivity, case_id)

        fix_params = {
            'Account': client,
            'HandlInst': "3",
            'Side': "2",
            'OrderQty': qty,
            'TimeInForce': "0",
            'OrdType': 2,
            'Price': price,
            'TransactTime': time,
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'Currency': 'EUR',
            'SecurityExchange': 'XPAR',
        }
        fix_message = FixMessage(fix_params)
        fix_message.add_random_ClOrdID()
        fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)

    # endregion
    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    main_order_id = ExtractionDetail("order_id", "Order ID")
    client_order_id = ExtractionDetail("order_id", "ClOrdID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            main_order_id,
                                                                                            client_order_id
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent"),
                                                  verify_ent("Qty", order_qty.name, qty),
                                                  verify_ent("LmtPrice", order_price.name, price)
                                                  ]))
    # endregion
    # region Accept CO
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Check values in OrderBook after Accept
    request = call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open")]))
    # endregion
    # region Amend order
    fix_modify_message = deepcopy(fix_message)
    fix_modify_message.change_parameters({'Price': price2, 'OrderQty': qty2})

    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    amend_responce = fix_manager_qtwquod5.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message)
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Cancel order
    order_id = request[client_order_id.name]
    cancel_parms = {
        "ClOrdID": order_id,
        "Account": client,
        "Side": "2",
        "TransactTime": datetime.utcnow().isoformat(),
        "OrigClOrdID": order_id
    }
    fix_cancel = FixMessage(cancel_parms)
    responce_cancel = fix_manager_qtwquod5.Send_OrderCancelRequest_FixMessage(fix_cancel)
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Check values after Cancel
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled"),
                                                  verify_ent("Qty", order_qty.name, qty2),
                                                  verify_ent("LmtPrice", order_price.name, price2)
                                                  ]))
    # endregion
