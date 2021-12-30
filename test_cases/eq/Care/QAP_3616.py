import logging

from th2_grpc_act_gui_quod.order_book_pb2 import ExtractManualCrossValuesRequest

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.order_book_wrappers import ManualCrossDetails
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3616"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = "30"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    last_mkt = 'DASI'
    selected_rows = [1, 2]
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
    # endregion
    # region accept 1 order
    # eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # region accept 2 order
    # eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region manual_cross
    act2 = Stubs.win_act_order_book
    error_message = ExtractManualCrossValuesRequest.ManualCrossExtractedValue()
    error_message.name = "ErrorMessage"
    error_message.type = ExtractManualCrossValuesRequest.ManualCrossExtractedType.ERROR_MESSAGE
    request = ExtractManualCrossValuesRequest()
    request.extractionId = "ManualCrossErrorMessageExtractionID"
    request.extractedValues.append(error_message)
    manual_cross_details = ManualCrossDetails()
    manual_cross_details.set_default_params(base_request)
    manual_cross_details.set_price('0')
    manual_cross_details.set_last_mkt(last_mkt)
    manual_cross_details.set_quantity(qty)
    manual_cross_details.set_selected_rows({1,2})
    manual_cross_details.manualCrossValues.CopyFrom(request)

    response = call(act2.manualCross, manual_cross_details.build())
    print(response)
    # verifier = Verifier(case_id)
    # verifier.set_event_name("Check value")
    # verifier.compare_values('Error', response, "gtr")
    # verifier.verify()
