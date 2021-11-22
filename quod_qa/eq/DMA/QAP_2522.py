import logging
from datetime import datetime

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_fix_wrappers
from quod_qa.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_book_wrappers import OrdersDetails
from win_gui_modules.utils import get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "1"
    price = "0.0001"
    freenotes_expected_text = "11673 'Price' (0.0001) must be a multiple of the instrument's tick size (0.001)"
    # endregion

    # region Open FE
    case_name = "QAP-2522"
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

    # region Create order via FIX
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS('fix-bs-310-columbia', "XPAR_CLIENT1")
    connectivity = eq_fix_wrappers.buy_connectivity
    fix_manager_qtwquod5 = FixManager(connectivity, case_id)

    fix_params = {
        'Account': "CLIENT1",
        'HandlInst': "2",
        'Side': "2",
        'OrderQty': qty,
        'TimeInForce': "0",
        'Price': price,
        'OrdType': "2",
        'TransactTime': datetime.utcnow().isoformat(),
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
    rule_manager.remove_rule(nos_rule)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_freenotes = ExtractionDetail("order_freenotes", "FreeNotes")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "LmtPrice")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            order_freenotes])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Rejected"),
                                                  verify_ent("Order Qty", order_qty.name, qty),
                                                  verify_ent("Order Price", order_price.name, price),
                                                  verify_ent("FreeNotes", order_freenotes.name,
                                                             freenotes_expected_text)]))
    # endregion
