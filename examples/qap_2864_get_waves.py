from utils.services import Services
from utils.base_test import BaseTest
from utils.wrappers import *


class QAP_2864(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "QAP-2864",
                               "[WIN] Verify that TWAP algo takes into account RoundLot at scheduling time (the "
                               "Number of Slices is defined)")

    def execute(self):

        call = self.call

        set_base(self._session_id, self._event_id)

        common_act = self._services.main_win_service

        extraction_id = "getOrderAnalysisAlgoParameters"
        call(common_act.getOrderAnalysisAlgoParameters,
             order_analysis_algo_parameters_request(extraction_id, ["TWAP.waves", "Waves"]))
        call(common_act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                     [verify_ent("Waves", "Waves", "4")]))
