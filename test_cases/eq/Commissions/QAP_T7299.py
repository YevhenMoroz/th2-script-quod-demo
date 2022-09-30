import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, TradeBookColumns, \
    SecondLevelTabs, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7299(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.client = self.data_set.get_client_by_name("client_fees_1")
        self.client_acc = self.data_set.get_account_by_name("client_fees_1_acc_1")
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters({'Account': self.client})
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.booking_win = OMSBookingWindow(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send commission
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.send_default_fee()
        # endregion
        # region send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion
        # region exec order
        self.order_book.manual_execution(filter_dict={OrderBookColumns.order_id.value: order_id})
        self.order_book.check_order_fields_list({OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region complete and book order
        self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order_id])
        rate = self.order_book.extract_sub_lvl_fields([TradeBookColumns.fee_rate.value],
                                                      [TradeBookColumns.misc_tab.value],
                                                      {OrderBookColumns.order_id.value: order_id})
        self.order_book.compare_values({TradeBookColumns.fee_rate.value: "1"}, rate, "Compare Rate")

        self.mid_office.book_order([OrderBookColumns.order_id.value, order_id])
        total_fee = self.mid_office.extract_block_field(MiddleOfficeColumns.total_fees.value,
                                                        [MiddleOfficeColumns.order_id.value, order_id])
        self.mid_office.compare_values({MiddleOfficeColumns.total_fees.value: "1"}, total_fee, "Compare total fee")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()

