from utils.services import Services
from utils.base_test import BaseTest
from utils.wrappers import *


class PVExample(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "QAP-2838-step-4", "Get Order Analysis Audit Events")

    def execute(self):
        call = self.call
        set_base(self._session_id, self._event_id)
        common_act = self._services.main_win_service

        extraction_id = "getOrderAnalysisAlgoParameters"

        call(common_act.getOrderAnalysisAlgoParameters,
             order_analysis_algo_parameters_request(extraction_id, ["PercentageVolume"], {"Owner": "annab"}))
        call(common_act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                     [verify_ent("PercentageVolume", "PercentageVolume", "40.0")]))
