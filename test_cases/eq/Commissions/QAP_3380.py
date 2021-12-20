import logging
import os
import time

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom.basic_custom_actions import create_event
from rule_management import RuleManager
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import CommissionClients, CommissionAccounts
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_3380(TestCase):

    def __init__(self, report_id, session_id):
        super().__init__(report_id, session_id)
        session_alias = SessionAliasOMS()
        self.ss_connectivity = session_alias.ss_connectivity
        self.bs_connectivity = session_alias.bs_connectivity
        self.wa_connectivity = session_alias.wa_connectivity
        self.qty = "200"
        self.price = "10"
        self.client = CommissionClients.CLIENT_COMM_1.value
        self.account = CommissionAccounts.CLIENT_COMM_1_SA1
        self.case_id = create_event(os.path.basename(__file__)[:-3], self.report_id)

    @decorator_try_except(test_id=os.path.basename(__file__)[:-3])
    def execute(self):
        main_window = BaseMainWindow(self.case_id, self.session_id)
        order_book = OMSOrderBook(self.case_id, self.session_id)
        middle_office = OMSMiddleOfficeBook(self.case_id, self.session_id)
        RestCommissionsSender(self.wa_connectivity, self.case_id).clear_commissions()
        self.__open_front_end(main_window, self.report_id)
        self.__send_fix_orders()
        print("Sent")
        split_param_1 = order_book.create_split_booking_parameter("100", comm_basis="Absolute", comm_rate="5",
                                                                  fee_type="ExchFees", fee_basis="Absolute",
                                                                  fee_rate="5")
        split_param_2 = order_book.create_split_booking_parameter()
        order_book.split_book([split_param_1, split_param_2])
        self.__verify_commissions(middle_office)

    def __send_fix_orders(self):
        no_allocs: dict = {"NoAllocs": [{'AllocAccount': self.account.value, 'AllocQty': self.qty}]}
        try:
            rule_manager = RuleManager()
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(
                self.bs_connectivity, self.client + '_EUREX', "XEUR", float(self.price), float(self.price),
                int(self.qty),
                int(self.qty), 1)
            fix_manager = FixManager(self.ss_connectivity, self.case_id)
            new_order_single1 = FixMessageNewOrderSingleOMS().set_default_dma_limit_eurex().add_ClordId(
                (os.path.basename(__file__)[:-3])).change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price, "Account": self.client,
                 'PreAllocGrp': no_allocs})
            self.response: list = fix_manager.send_message_and_receive_response_fix_standard(new_order_single1)
        finally:
            time.sleep(2)
            rule_manager.remove_rule(nos_rule)

    @staticmethod
    def __open_front_end(main_window, report_id):
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        main_window.open_fe(report_id, work_dir, username, password)

    @staticmethod
    def __verify_commissions(middle_office: OMSMiddleOfficeBook):
        commissions = middle_office.extracting_values_from_amend_ticket(
            [
                PanelForExtraction.COMMISSION,
                PanelForExtraction.FEES
            ])
        parsed_comm = middle_office.split_2lvl_values(commissions)
        fees_expected = {'FeeType': 'ExchFees', 'Basis': 'Absolute', 'Rate': '2.5', 'Amount': '2.5', 'Currency': 'EUR',
                         'Category': 'Other'}
        commissions_expected = {'Basis': 'Absolute', 'Rate': '2.5', 'Amount': '2.5', 'Currency': 'EUR'}
        for extract_dict in parsed_comm:
            if 'FeeType' in extract_dict:
                fees_actual = extract_dict
                middle_office.compare_values(fees_expected, fees_actual, "Fees verifying")
            else:
                commissions_actual = extract_dict
                middle_office.compare_values(commissions_expected, commissions_actual, "Commissions verifying")
