import logging
import os
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import TradeBookColumns, MiddleOfficeColumns, \
    AllocationsColumns, ClientInboxColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7390(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "4232"
        self.price = "4232"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.test_id = create_event(self.__class__.__name__, self.report_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.trades = OMSTradesBook(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(recalculate=True).change_message_params(
            {"venueID": self.data_set.get_venue_by_name("venue_2")}).send_post_request()
        self.__send_fix_orders()

        self.cl_inbox.accept_order(filter={ClientInboxColumns.order_id.value: self.order_id})
        self.order_book.manual_execution(filter_dict={OrderBookColumns.order_id.value: self.order_id})
        filter_list = [OrderBookColumns.order_id.value, self.order_id]
        self.order_book.complete_order(filter_list=filter_list)
        self.__verify_fees_of_executions()
        self.middle_office.set_modify_ticket_details(remove_fee=True)
        self.middle_office.book_order(filter=filter_list)
        self.__verify_fees_in_middle_office()
        self.middle_office.approve_block(filter_list=filter_list)
        self.middle_office.allocate_block(filter=filter_list)
        self.__verify_fees_in_allocation_ticket()

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit(
            "instrument_3").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
            {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
             'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2")})
        self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)
        self.order_id = self.response[0].get_parameter("OrderID")

    def __verify_fees_of_executions(self):
        self.trades.set_filter(["Order ID", self.order_id])
        fees = {TradeBookColumns.exec_fees.value: self.trades.extract_field(TradeBookColumns.exec_fees.value)}
        self.trades.compare_values({TradeBookColumns.exec_fees.value: ""}, fees, event_name='Check values')

    def __verify_fees_in_middle_office(self):
        fees = self.middle_office.extract_block_field(MiddleOfficeColumns.total_fees.value,
                                                      filter_list=[MiddleOfficeColumns.order_id.value, self.order_id])
        self.middle_office.compare_values({MiddleOfficeColumns.total_fees.value: ""}, fees, event_name='Check values')

    def __verify_fees_in_allocation_ticket(self):
        fees = self.middle_office.extract_allocate_value(AllocationsColumns.total_fees.value)
        self.middle_office.compare_values({AllocationsColumns.total_fees.value: "0.01"}, fees,
                                          event_name='Check values')
