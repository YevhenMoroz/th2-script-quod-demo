import logging

from th2_grpc_act_gui_quod import order_book_pb2

from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.order_book_wrappers import ManualCrossDetails, ManualCrossExtractedValue, \
    ExtractManualCrossValuesRequest
from win_gui_modules.utils import get_base_request, call

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3616"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    case_id = create_event(case_name, report_id)
    # endregion
    # region create order via fix
    qty = "800"
    price = "30"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    recipient = 'Desk of SalesDealers 1 (CL)'
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, 'Limit', 'Day', True, recipient, price, is_sell=True)
    # endregion
    # region accept 1 order
    eq_wrappers.suspend_order(base_request, False)
    # endregion
    eq_wrappers.create_order(base_request, qty, client, lookup, 'Limit', 'Day', True, recipient, price, is_sell=False)
    # region accept 2 order
    eq_wrappers.scroll_order_book(base_request, 1)
    eq_wrappers.suspend_order(base_request, False)
    # endregion
    # region manual_cross
    manual_cross_extracted_values = [
        ManualCrossExtractedValue(order_book_pb2.ExtractManualCrossValuesRequest.ManualCrossExtractedType.ERROR_MESSAGE,
                                  'Error').build()

    ]
    extract_manual_cross_value_request = ExtractManualCrossValuesRequest('1', manual_cross_extracted_values).build()
    manual_cross_details = ManualCrossDetails(base_request)
    manual_cross_details.set_price('20')
    manual_cross_details.set_extract_manual_cross_value(extract_manual_cross_value_request)
    manual_cross_details.set_quantity('800')
    manual_cross_details.set_last_mkt('XASE')
    manual_cross_details.set_capacity('Agency')
    manual_cross_details.set_selected_rows([1, 2])

    response = call(Stubs.win_act_order_book.manualCross, manual_cross_details.build())
    print(response)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View",
                            'Error - [QUOD-11503] Invalid status [SuspendedCare=Y]', response['Error']
                            )
    verifier.verify()
