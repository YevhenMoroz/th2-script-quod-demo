import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns,  \
    MiddleOfficeColumns, ExecSts, DoneForDays, PostTradeStatuses, ConfirmationServices
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7160(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.client = self.data_set.get_client_by_name('client_pt_9')
        self.fix_message.change_parameter('Account', self.client)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        self.order_id = response[0].get_parameter("OrderID")
        self.client_inbox.accept_order()
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        #  endregion
        # region ececute  order
        self.order_book.manual_execution()
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        #  endregion
        # region complete and book order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, self.order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
             OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        self.mid_office.book_order([OrderBookColumns.order_id.value, self.order_id])
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id]).check_order_fields_list(
            {OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
             OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        self.__check_middle_office_field({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.appr_pending_sts.value,
                                          MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.unmatched_sts.value})
        #  endregion
        # region override confirmation service
        self.mid_office.override_confirmation_service({OrderBookColumns.order_id.value: self.order_id})
        self.__check_middle_office_field({MiddleOfficeColumns.conf_service.value: ConfirmationServices.manual.value})
        #  endregion

    def __check_middle_office_field(self, list_of_value: dict):
        for i, y in list_of_value.items():
            res = self.mid_office.extract_block_field(i,
                                                      filter_list=[OrderBookColumns.order_id.value, self.order_id])
            self.mid_office.compare_values({i: y}, {i: res[i]}, 'Check field from Middle Office')
