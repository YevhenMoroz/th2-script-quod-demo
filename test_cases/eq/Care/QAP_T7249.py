import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, Status, \
    ExecSts, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7249(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '100'
        self.price = '10'
        self.client = self.data_set.get_client('client_pt_1')
        self.venue_client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.booking_blotter = OMSBookingWindow(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.rest_api_manager = RestCommissionsSender(self.rest_api_connectivity, self.test_id, self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (precondition)
        self.fix_message.set_default_care_market('instrument_1')
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client,
             'TimeInForce': '6', 'ExpireDate': (datetime.now()).strftime("%Y%m%d")})

        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)
        # endregion

        # region split and partially filled CO order
        cum_qty = str(int(int(self.qty) / 2))
        try:
            nos_rule = self.rule_manager.add_NewOrdSingle_Market_FIXStandard(self.fix_env.buy_side,
                                                                             self.venue_client, self.mic, False,
                                                                             int(cum_qty), float(self.price))
            self.order_ticket.set_order_details(qty=cum_qty)
            self.order_ticket.split_order(filter_list)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        # endregion
        self.order_book.manual_execution(filter_dict=filter_dict, qty=cum_qty, price=self.price)
        # region check executions
        self.order_book.set_filter(filter_list).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        self.order_book.set_filter(filter_list).check_second_lvl_fields_list(
            {OrderBookColumns.sts.value: ExecSts.eliminated.value})
        # endregion
        self.order_book.complete_order(filter_list=filter_list)
        self.middle_office.book_order(filter=filter_list)
        self.middle_office.approve_block(filter_list=filter_list)
        no_allocs = [{AllocationsColumns.security_acc.value: self.alloc_account,
                      AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=no_allocs)
        self.middle_office.allocate_block(filter=filter_list)
        # region Checking values in Allocations
        extracted_fields = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value])
        self.middle_office.compare_values(
            {AllocationsColumns.sts.value: 'Affirmed', AllocationsColumns.match_status.value: 'Matched'},
            extracted_fields, 'Checking values in Allocations')
        # endregion
        # region call end of day procedures
        self.ssh_client.send_command("~/quod/script/site_scripts/db_endOfDay_postgres")
        # endregion

        # region check ExpireOrders
        self.order_book.refresh_order(filter_list)
        self.order_book.set_filter(filter_list)
        values = self.order_book.extract_fields_list({OrderBookColumns.sts.value: OrderBookColumns.sts.value,
                                                      OrderBookColumns.free_notes.value: OrderBookColumns.free_notes.value,
                                                      OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value})
        self.order_book.compare_values({
            OrderBookColumns.sts.value: Status.expired.value,
            OrderBookColumns.free_notes.value: "Order terminated by Quod eod_ExpireOrders procedure",
            OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value
        }, values, 'Check Expired sts')
        # endregion
