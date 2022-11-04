from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX


class QAP_T8378(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_sell = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.quote_reject = FixMessageQuoteRequestRejectFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.wrong_client = "WRONG_CLIENT"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                            Account=self.client)
        response: list = self.fix_manager_sell.send_message_and_receive_response(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote_request)
        # endregion

        # region Step 2
        quote_id = response[0].get_parameter("QuoteID")
        self.quote_cancel.set_params_for_cancel(self.quote_request)
        # self.quote_cancel.change_parameter("QuoteID", quote_id)
        # self.quote_cancel.remove_parameter("QuoteReqID")
        self.fix_manager_sell.send_message(self.quote_cancel)
        self.fix_verifier.check_fix_message(self.quote_cancel)
        # endregion
        # region Step 3
        self.quote_request.set_rfq_params().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                            Account=self.wrong_client)
        self.fix_manager_sell.send_message_and_receive_response(self.quote_request)
        text = "11620 unknown client WRONG_CLIENT"
        self.quote_reject.set_quote_reject_params(self.quote_request, text=text)
        self.quote_reject.remove_fields_in_repeating_group("NoRelatedSymbols", ["Account", "OrderQty"])
        self.fix_verifier.check_fix_message(self.quote_reject)
        # endregion
