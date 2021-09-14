import logging
from datetime import datetime

from th2_grpc_act_gui_quod.act_ui_win_pb2 import DirectChildCareDetails

from quod_qa.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, ModifyOrderDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request, BaseParams
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-3875"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "40"
    client = "CLIENTSKYLPTOR"
    lookup = "PROL"
    last_mkt = 'DASI'
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create 1 CO order
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)

    # endregion
    # region create 2 CO order
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)

    # endregion
    # region create 3 CO order
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)

    # endregion

    # region DirectChildCare these orders
    eq_wrappers.direct_child_care_order('100', 'ChiX direct access', recipient='vskulinec', count=3)
    # endregion
