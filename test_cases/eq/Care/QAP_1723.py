import logging

from win_gui_modules.order_ticket import ExtractOrderTicketValuesRequest, OrderTicketExtractedValue
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from win_gui_modules.utils import get_base_request, call

from custom.verifier import Verifier
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType, OrderBookColumns, DiscloseExec, TimeInForce
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_1723(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.desk = environment.get_list_fe_environment()[0].desk_3
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.price = "50"
        self.qty = "800"
        self.client = self.data_set.get_client_by_name('client_co_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.order_type = OrderType.limit.value
        self.base_request = get_base_request(self.session_id, self.test_id)


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region create order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, order_type=self.order_type,
                                            tif= TimeInForce.DAY.value, is_sell_side=False, instrument=self.lookup,
                                            recipient=self.desk, disclose_flag=2)
        self.order_ticket.create_order(lookup=self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region check disclose execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.disclose_exec.value: DiscloseExec.real_time.value})
        # endregion
        # request = ExtractOrderTicketValuesRequest(self.base_request)
        # request.get_disclose_flag_state()
        # result = call(Stubs.win_act_order_ticket.extractOrderTicketValues, request.build())
        result = self.order_ticket.check_availability(["DISCLOSE_FLAG"])
        verifier = Verifier(self.test_id)
        verifier.set_event_name("Check value")
        verifier.compare_values("Availability Disclose flag in order ticket", "False", result["DISCLOSE_FLAG"])
        verifier.verify()



