import logging

from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum, ExtractOrderTicketValuesRequest

from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1723"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "800"
    price = "50"
    client = "CLIENT_FIX_CARE"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region create order with account
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    # region Create CO order
    eq_wrappers.create_order(base_request, qty, client, 'VETO', 'Limit', 'Day', True, username, price,
                             disclose_flag=DiscloseFlagEnum.REALTIME)
    # endregion
    # region check value disclose flag in orderbook
    eq_wrappers.verify_order_value(base_request, case_id, 'DiscloseExec', 'R')
    disclose_flag_value = ExtractOrderTicketValuesRequest.OrderTicketExtractedValue()
    disclose_flag_value.type = ExtractOrderTicketValuesRequest.OrderTicketExtractedType.DISCLOSE_FLAG
    disclose_flag_value.name = "DiscloseFlag"

    request = ExtractOrderTicketValuesRequest()
    request.base.CopyFrom(base_request)
    request.extractionId = "DiscloseFlagExtractionID"
    request.extractedValues.append(disclose_flag_value)
    result = call(Stubs.win_act.extractOrderTicketValues, request)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Disable', True, result)
    verifier.verify()
