import logging
from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request, prepare_fe, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1068"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "10"
    lookup = "VETO"
    client = "MOClient"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
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
    '''
    # region Create CO
    quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 1, qty, 0)

    # region AcceptOrder
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingle_Market(eq_wrappers.buy_connectivity, client + '_PARIS', 'XPAR',
                                                    trade=False, tradedQty=int(qty), avgPrice=float(price))

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open")
                                                  ]))
    # endregion

    # region DirectMOC split
    try:
        eq_wrappers.direct_moc_order('50', 'ChiX direct access')
    finally:
        rule_manager.remove_rule(nos_rule)
    # endregion
    '''
    # check sub Order status
    eq_wrappers.verify_order_value(base_request, case_id, "Order Status", "Eliminated", True)
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", str(int(int(qty) / 2)), True)
    # endregion
    # region Close FE
    # close_fe(case_id, session_id)
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    # endregion
