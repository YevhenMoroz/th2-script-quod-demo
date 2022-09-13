import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7432(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.route = self.data_set.get_route('route_2')
        self.client_id = self.fix_message.get_parameter('ClOrdID')
        self.user = environment.get_list_fe_environment()[0].user_1
        self.route = self.data_set.get_route("route_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create first CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id1 = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion
        # region create first CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id2 = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion
        # region create first CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id3 = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion
        # region direct 3 CO
        self.order_book.direct_child_care_order("100", self.user, self.route, selected_rows=[1,2,3], filter_dict={OrderBookColumns.cl_ord_id.value: self.client_id})
        # endregion
        # region check child and order fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_second_lvl_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region check child and order fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_second_lvl_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region check child and order fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id3]).check_order_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id3]).check_second_lvl_fields_list({OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
