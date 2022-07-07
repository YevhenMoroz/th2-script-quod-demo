import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, OrderType, TimeInForce
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_3998(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = "1000"
        self.price ="50"
        self.fix_message.change_parameters(['OrderQtyData', {'OrderQty': self.qty}, "Price", self.price])
        self.lookup = "DNX"
        self.route = self.data_set.get_route("route_1")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty_type = self.data_set.get_qty_type('qty_type_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        # region do direct child care
        self.order_book.extract_error_from_order_ticket


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