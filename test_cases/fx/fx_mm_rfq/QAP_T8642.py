from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestSynergyFX import FixMessageQuoteRequestSynergyFX


class QAP_T8642(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_cnx
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestSynergyFX(data_set=self.data_set)
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.party = [{
            "PartyID": self.client,
            "PartyIDSource": "D",
            "PartyRole": "1"
        }]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_synergy_params()
        self.quote_request.update_value_in_repeating_group("NoRelatedSym", "NoPartyIDs", self.party)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region step 2
        self.sleep(120)
        self.quote_cancel.set_params_for_receive_synergy(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote_cancel)
