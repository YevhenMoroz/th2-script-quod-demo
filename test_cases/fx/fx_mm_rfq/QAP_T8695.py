from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX


class QAP_T8695(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_reject = FixMessageQuoteRequestRejectFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.account = self.data_set.get_client_by_name("client_mm_4")
        self.text_1 = "11613 'Side': undefined error, according to 'LegSide' presence"
        self.text_2 = "11613 'Side': B error, according to 'LegSide' presence"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Side="1")
        self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 2
        self.quote_request.set_swap_rfq_params()
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].pop('LegSide')
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].pop('LegSide')
        self.quote_request.get_parameter("NoRelatedSymbols")[0].pop('Side')
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].update({'LegSide': "#"})
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].update({'LegSide': "#"})
        self.quote_request.change_parameters({"BidSwapPoints": "*",
                                              "BidPx": "*",
                                              "Side": "#"})
        self.quote.set_params_for_quote_swap(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 3
        self.quote_request.set_swap_rfq_params()
        self.quote_request.update_near_leg(leg_side="2")
        self.quote_request.update_far_leg(leg_side="1")
        self.quote_request.get_parameter("NoRelatedSymbols")[0].pop('Side')
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote_request.change_parameters({"QuoteType": "1"})
        self.quote_reject.set_quote_reject_params(self.quote_request, text=self.text_1)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(fix_message=self.quote_reject, key_parameters=["QuoteReqID"])
        # endregion
        # region Step 4
        self.quote_request.set_swap_rfq_params()
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].pop('LegSide')
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].pop('LegSide')
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account)
        self.fix_manager_gtw.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0].update({'LegSide': "#"})
        self.quote_request.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1].update({'LegSide': "#"})
        self.quote_request.change_parameters({"QuoteType": "1"})
        self.quote_reject.set_quote_reject_params(self.quote_request, text=self.text_2)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(fix_message=self.quote_reject, key_parameters=["QuoteReqID"])
        # endregion
