import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_book_wrappers import OrdersDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3434"
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "30"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    last_mkt = 'DASI'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create order via fix
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    order_id2 = eq_wrappers.get_order_id(base_request)
    # endregion
    # region accept 1 order
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # region accept 2 order
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region manual_cross
    eq_wrappers.manual_cross_orders(base_request, qty, price, (1, 2), last_mkt)
    # endregion
    # region check order1
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_exec_sts = ExtractionDetail('order_exec_sts', 'ExecSts')
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_exec_sts
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order ExecSts", order_exec_sts.name, "Filled")
                                                  ]))
    # endregion
    # region filter and check 2 order
    order_info_extraction_cancel = "getOrderInfo_cancelled"

    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    main_order_details.set_extraction_id(order_info_extraction_cancel)
    main_order_details.set_filter(["Order ID", order_id2])
    order_exec_sts = ExtractionDetail('order_exec_sts', 'ExecSts')
    main_order_details.add_single_order_info(OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                             order_exec_sts
                                                                             ])))

    call(act.getOrdersDetails, main_order_details.request())
    call(common_act.verifyEntities, verification(order_info_extraction_cancel, "checking order2",
                                                 [verify_ent("Order ExecSts", order_exec_sts.name, "Filled")]))
