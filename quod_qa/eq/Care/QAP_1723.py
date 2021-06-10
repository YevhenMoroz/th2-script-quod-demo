import logging
from datetime import datetime

from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum, ExtractOrderTicketValuesRequest

from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2550"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "800"
    client = "CLIENTSKYLPTOR"
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region create order with account
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # region Create CO order
    eq_wrappers.create_order(base_request, qty, client, 'VETO', 'Limit', 'Day', True, 'vskulinec','50', False, False,
                             False, DiscloseFlagEnum.REALTIME, None)
    # endregion
    # region check value disclose flag in orderbook
    eq_wrappers.verify_value(base_request, case_id, 'DiscloseExec', 'R')
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
