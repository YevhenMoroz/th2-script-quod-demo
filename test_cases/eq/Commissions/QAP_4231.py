import logging
import os
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.fe_trading_constant import TradeBookColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_4231(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "4231"
        self.price = "4231"
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.account = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.case_id = create_event(self.__class__.__name__, self.report_id)
        self.trades = OMSTradesBook(self.case_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.case_id)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)

    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(recalculate=True,
                                                                         account=self.account).send_post_request()
        self.__send_fix_orders()
        self.__verify_commissions_of_executions(self.trades)
        self.middle_office.set_modify_ticket_details(remove_comm=True)
        self.middle_office.book_order()
        self.__verify_fees_in_middle_office(self.middle_office)
        self.middle_office.approve_block()
        self.middle_office.allocate_block()
        self.__verify_fees_in_allocation_ticket(self.middle_office)

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account, 'AllocQty': self.qty}]}
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, self.client + '_EUREX', "XEUR", float(self.price), float(self.price),
                int(self.qty), int(self.qty), 1)
            new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit(
                "instrument_2").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2")})
            self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    def __verify_commissions_of_executions(self, trades: OMSTradesBook):
        self.order_id = self.response[0].get_parameter("OrderID")
        trades.set_filter(["Order ID", self.order_id])
        commissions = {
            TradeBookColumns.client_commission.value: trades.extract_field(TradeBookColumns.client_commission.value)}
        trades.compare_values({TradeBookColumns.client_commission.value: ""}, commissions,
                              event_name='Check values')

    def __verify_fees_in_middle_office(self, middle_office: OMSMiddleOffice):
        commission = middle_office.extract_block_field(MiddleOfficeColumns.client_comm.value,
                                                       [MiddleOfficeColumns.order_id.value, self.order_id])
        middle_office.compare_values({MiddleOfficeColumns.client_comm.value: ""}, commission, event_name='Check values')

    def __verify_fees_in_allocation_ticket(self, middle_office: OMSMiddleOffice):
        commission = middle_office.extract_allocate_value(AllocationsColumns.client_comm.value, self.account)
        middle_office.compare_values({AllocationsColumns.client_comm.value: "1.123"}, commission,
                                     event_name='Check values')
