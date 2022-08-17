import logging
import os
import time
from pathlib import Path

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.DataSet import CommissionClients, CommissionAccounts
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7512(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "3310"
        self.price = "3310"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1
        self.case_id = create_event(self.__class__.__name__, self.report_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id, self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_manager = FixManager(self.ss_connectivity, self.case_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.send_default_fee()
        self.__send_fix_orders()
        self.middle_office.book_order()
        self.middle_office.set_modify_ticket_details(remove_fee=True)
        self.middle_office.amend_block()
        self.__verify_fees(self.middle_office)

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account.value, 'AllocQty': self.qty}]}
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.data_set.get_venue_client_names_by_name(
                                                                             "client_com_1_venue_2"),
                                                                         self.data_set.get_mic_by_name("mic_2"),
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit(
                "instrument_3").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2")})
            self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)
            self.order_id = self.response[0].get_parameter("OrderID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    def __verify_fees(self, middle_office: OMSMiddleOffice):
        total_fees = MiddleOfficeColumns.total_fees.value
        fees = middle_office.extract_block_field(total_fees, [MiddleOfficeColumns.order_id.value, self.order_id])
        middle_office.compare_values({total_fees: ""}, fees, event_name='Check values')
