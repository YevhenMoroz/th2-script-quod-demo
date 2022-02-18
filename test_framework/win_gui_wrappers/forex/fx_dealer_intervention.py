from custom.verifier import VerificationMethod
from stubs import Stubs
from test_framework.win_gui_wrappers.base_dealer_intervention import BaseDealerIntervention
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    RFQExtractionDetailsRequest, ModificationRequest


class FXDealerIntervention(BaseDealerIntervention):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.base_data = BaseTableDataRequest(base=self.base_request)
        self.extraction_request = ExtractionDetailsRequest(self.base_data)
        self.rfq_extraction_request = RFQExtractionDetailsRequest(base=self.base_request)
        self.modification_request = ModificationRequest(base=self.base_request)
        self.service = Stubs.win_act_dealer_intervention_service
        self.assign_to_me_call = self.service.assignToMe
        self.un_assign_to_me_call = self.service.unAssign
        self.estimate_call = self.service.estimate
        self.modify_call = self.service.modifyAssignedRFQ
        self.getAssignedDetails_call = self.service.getAssignedRFQDetails
        self.getUnAssignedDetails_call = self.service.getUnassignedRFQDetails
        self.getRFQDetail_call = self.service.getRFQDetails
        self.set_default_params()

    def compare_values(self, expected_value: str, actual_value: str, event_name: str = "Compare values",
                       ver_method: VerificationMethod = VerificationMethod.EQUALS, value_name: str = "Value"):
        self.verifier.set_event_name(event_name)
        self.verifier.compare_values(value_name, expected_value, actual_value, ver_method)
        self.verifier.verify()