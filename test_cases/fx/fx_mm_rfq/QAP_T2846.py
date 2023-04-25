from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.fx.fx_wrapper.common_tools import extract_freenotes, check_quote_status, extract_automatic_quoting, \
    check_quote_request_id
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixQuoteRequestFX import FixQuoteRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook


class QAP_T2846(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_manager_fh = FixManager(self.fh_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.settle_type_spot = self.data_set.get_settle_type_by_name("spot")
        self.sec_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.settle_date_tod = self.data_set.get_settle_date_by_name("today")
        self.settle_type_tod = self.data_set.get_settle_type_by_name("today")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.expected_notes = "request exceeds quantity threshold for instrument over this client tier"
        self.expected_quoting = "Y"
        self.md_req_id_sp = "EUR/USD:SPO:REG:HSBC"
        self.exceed_threshold_qty = "40000000"
        self.exceed_threshold_uneven_qty = "50000000"
        self.uneven_qty = "2000000"
        self.no_side = ""
        self.key_parameter = "quoterequestid"
        self.quote_state = "unavailablepricestate"
        self.quote_state_cause = "unavailablepricecause"
        self.response = None
        self.quote_cancel = FixMessageQuoteCancelFX()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.quote_request.update_near_leg(leg_qty=self.exceed_threshold_qty)
        self.quote_request.update_far_leg(leg_qty=self.exceed_threshold_qty)
        self.fix_manager_sel.send_message(self.quote_request)
        # region Step 3
        quote_status = extract_automatic_quoting(self.quote_request)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Even Swap 40m RFQ")
        self.verifier.compare_values("AutomaticQuoting", "N", quote_status)
        self.verifier.verify()
        # endregion
        # endregion
        # region Step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.response = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # region Step 3
        quote_status = extract_automatic_quoting(self.quote_request)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Even Swap 1m RFQ")
        self.verifier.compare_values("AutomaticQuoting", "Y", quote_status)
        self.verifier.verify()
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager_sel.send_message(self.quote_cancel)
        # endregion
        # region Step 3
        # endregion
        # region Step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.quote_request.update_far_leg(leg_qty=self.uneven_qty)
        self.response = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # region Step 3
        quote_status = extract_automatic_quoting(self.quote_request)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Uneven Swap 1m/2m RFQ")
        self.verifier.compare_values("AutomaticQuoting", "Y", quote_status)
        self.verifier.verify()
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager_sel.send_message(self.quote_cancel)
        # endregion
        # region Step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.quote_request.update_near_leg(leg_qty=self.exceed_threshold_qty)
        self.quote_request.update_far_leg(leg_qty=self.exceed_threshold_uneven_qty)
        self.fix_manager_sel.send_message(self.quote_request)
        # region Step 3
        quote_status = extract_automatic_quoting(self.quote_request)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Uneven Swap 40m/50m RFQ")
        self.verifier.compare_values("AutomaticQuoting", "N", quote_status)
        self.verifier.verify()
        # endregion
        # region Step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.quote_request.update_near_leg(leg_qty=self.exceed_threshold_qty, settle_date=self.settle_date_tod,
                                           settle_type=self.settle_type_tod, leg_sec_type=self.sec_type_fwd)
        self.quote_request.update_far_leg(leg_qty=self.exceed_threshold_uneven_qty, settle_date=self.settle_date_spot,
                                          settle_type=self.settle_type_spot, leg_sec_type=self.sec_type_spot)
        self.fix_manager_sel.send_message(self.quote_request)
        # region Step 3
        quote_status = extract_automatic_quoting(self.quote_request)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Uneven Swap Tod/Spot 40m/50m RFQ")
        self.verifier.compare_values("AutomaticQuoting", "N", quote_status)
        self.verifier.verify()
        # endregion
