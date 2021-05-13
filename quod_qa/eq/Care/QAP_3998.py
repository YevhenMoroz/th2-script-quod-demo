import logging
from datetime import datetime

from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest
from th2_grpc_hand import rhbatch_pb2

from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, close_fe, call
from win_gui_modules.wrappers import set_base, verification, verify_ent, direct_child_care, direct_moc_request, \
    direct_loc_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-3998"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    newQty = "100"
    price = "40"
    newPrice = "1"
    time = datetime.utcnow().isoformat()
    lookup = "PROL"
    client = "CLIENTSKYLPTOR"
    # endregion
    list_param = {'qty': qty, 'Price': newPrice}
    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregionA

    # region Create CO
    eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # endregion
    # region DirectChildCare split
    error_message = ExtractDirectsValuesRequest.DirectsExtractedValue()
    error_message.name = "ErrorMessage"
    error_message.type = ExtractDirectsValuesRequest.DirectsExtractedType.ERROR_MESSAGE
    request = ExtractDirectsValuesRequest()
    request.extractionId = "DirectErrorMessageExtractionID"
    request.extractedValues.append(error_message)
    response = call(Stubs.win_act_order_book.orderBookDirectChildCare,
                direct_child_care('UnmatchedQty', '0', '', 'ChiX direct access', request))
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Error_message', 'Error - Qty Percentage should be greater than zero (0)', response['ErrorMessage'])
    verifier.verify()
    # endregion