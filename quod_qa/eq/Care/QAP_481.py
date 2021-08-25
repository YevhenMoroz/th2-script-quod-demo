import logging
from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, direct_moc_request
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-481"
    # region Declarations
    qty = "900"
    lookup = "PROL"
    client = "CLIENT_FIX_CARE"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregionA
    # region Create CO
    eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 1, qty, 0)
    eq_wrappers.accept_order(lookup, qty, "")
    # endregion
    # region DirectMOC split
    error_message = ExtractDirectsValuesRequest.DirectsExtractedValue()
    error_message.name = "ErrorMessage"
    error_message.type = ExtractDirectsValuesRequest.DirectsExtractedType.ERROR_MESSAGE
    request = ExtractDirectsValuesRequest()
    request.extractionId = "DirectErrorMessageExtractionID"
    request.extractedValues.append(error_message)
    response = call(Stubs.win_act_order_book.orderBookDirectMoc,
                    direct_moc_request('UnmatchedQty', '0', 'ChiX direct access', request))
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Error_message', 'Error - Qty Percentage should be greater than zero (0)',
                            response['ErrorMessage'])
    verifier.verify()
