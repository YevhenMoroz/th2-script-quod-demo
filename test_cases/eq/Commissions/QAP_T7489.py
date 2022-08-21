import logging
import os
import time
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom.basic_custom_actions import create_event
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.DataSet import CommissionClients, CommissionAccounts
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7489(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.qty = "200"
        self.price = "10"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1
        self.test_id = create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.__send_fix_orders()
        split_param_1 = self.order_book.create_split_booking_parameter("100", comm_basis="Absolute", comm_rate="5",
                                                                       fee_type="ExchFees", fee_basis="Absolute",
                                                                       fee_rate="5")
        split_param_2 = self.order_book.create_split_booking_parameter()
        self.order_book.split_book([split_param_1, split_param_2])
        self.__verify_commissions()

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account.value, 'AllocQty': self.qty}]}
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, self.data_set.get_venue_client_names_by_name("client_com_1_venue_2"),
                self.data_set.get_mic_by_name("mic_2"), float(self.price), float(self.price), int(self.qty),
                int(self.qty), 1)
            new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit(
                "instrument_3").add_ClordId((os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 'PreAllocGrp': no_allocs, "ExDestination": self.data_set.get_mic_by_name("mic_2")})
            self.response: list = self.fix_manager.send_message_and_receive_response_fix_standard(new_order_single)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    def __verify_commissions(self):
        commissions = self.middle_office.extracting_values_from_amend_ticket(
            [
                PanelForExtraction.COMMISSION,
                PanelForExtraction.FEES
            ])
        parsed_comm = self.middle_office.split_fees(commissions)
        fees_expected = {'FeeType': 'ExchFees', 'Basis': 'Absolute', 'Rate': '2.5', 'Amount': '2.5', 'Currency': 'EUR',
                         'Category': 'Other'}
        commissions_expected = {'Basis': 'Absolute', 'Rate': '2.5', 'Amount': '2.5', 'Currency': 'EUR'}
        for extract_dict in parsed_comm:
            if 'FeeType' in extract_dict:
                fees_actual = extract_dict
                self.middle_office.compare_values(fees_expected, fees_actual, "Fees verifying")
            else:
                commissions_actual = extract_dict
                self.middle_office.compare_values(commissions_expected, commissions_actual, "Commissions verifying")
