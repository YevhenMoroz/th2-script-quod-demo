import logging
import os
from datetime import datetime, date, timedelta

from win_gui_modules.order_book_wrappers import OrdersDetails, ModifyOrderDetails, CancelOrderDetails

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# need to modify
def execute(report_id):
    case_name = "QAP-2005"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    price2 = "19"
    expireDate = date.today() + timedelta(2)
    time = datetime.utcnow().isoformat()
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

    # region Create order via FIX
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", "XPAR_CLIENT1")

    connectivity = 'gtwquod5'
    fix_manager_qtwquod5 = FixManager(connectivity, case_id)

    fix_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "2",
        'OrderQty': qty,
        'TimeInForce': "0",
        'ExpireDate': expireDate.strftime("%Y%m%d"),
        'OrdType': "2",
        'Price': price,
        'TransactTime': time,
        'ExDestination': 'CHIX',
        'Instrument': {
            'Symbol': 'FR0000125007_EUR',
            'SecurityID': 'FR0000125007',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'Currency': 'EUR',
        'SecurityExchange': 'TRERROR',
    }

    fix_message = FixMessage(fix_params)
    fix_message.add_random_ClOrdID()
    fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
    rule_manager.remove_rule(nos_rule)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_tif = ExtractionDetail("order_tif", "TIF")
    order_expireDate = ExtractionDetail("order_expireDate", "ExpireDate")
    order_ordType = ExtractionDetail("oder_ordType", "OrdType")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    order_leavesQty = ExtractionDetail("order_leavesQty", "LeavesQty")
    main_order_id = ExtractionDetail("order_id", "Order ID")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            order_tif,
                                                                                            order_expireDate,
                                                                                            order_ordType,
                                                                                            main_order_id
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("Qty", order_qty.name, qty),
                                                  #verify_ent("LeavesQty", order_leavesQty.name, qty),
                                                  verify_ent("LmtPrice", order_price.name, price),
                                                  verify_ent("TIF", order_tif.name, "Day"),
                                                  verify_ent("OrdType", order_ordType.name, "Limit")
                                                  ]))
    # endregion

    # region Amend order
    request = call(act.getOrdersDetails, order_details.request())
    order_id = request[main_order_id.name]
    if not order_id:
        raise Exception("Order id is not returned")
    order_amend = OrderTicketDetails()
    order_amend.set_stop_price(price2)
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request)
    amend_order_details.set_order_details(order_amend)
    amend_order_details.set_filter(["Order ID", order_id])
    call(act.amendOrder, amend_order_details.build())
    # endregion

    # region Check values after Amending
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("LmtPrice", order_price.name, price2),
                                                  verify_ent("TIF", order_tif.name, "Day"),
                                                  ]))
    # endregion

    # region Cancelling order
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_filter(["Order ID", order_id])
    cancel_order_details.set_comment("Order cancelled by script")
    cancel_order_details.set_cancel_children(True)

    call(act.cancelOrder, cancel_order_details.build())
    # endregion

    # region Check values after Cancel
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled"),
                                                  verify_ent("TIF", order_tif.name, "Day"),
                                                  #verify_ent("LeavesQty", order_leavesQty.name, "")
                                                  ]))
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")