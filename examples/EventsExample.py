from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
from utils.base_test import BaseTest
from utils.services import Services
from utils.wrappers import *


class EventsExample(BaseTest):

    def __init__(self, services: Services, parent_event):
        super().__init__(services)
        self.create_test_event(parent_event, "QAP-2838-step-4", "Get Order Analysis Audit Events")

    def execute(self):
        call = self.call
        set_base(self._session_id, self._event_id)
        common_act = self._services.main_win_service

        extraction_id = "getOrderAnalysisEvents"
        call(common_act.getOrderAnalysisEvents,
             create_order_analysis_events_request(extraction_id, {"Owner": "annab"}))
        call(common_act.verifyEntities, verification(extraction_id, "checking order events",
                                                     [verify_ent("Event 1 ID", "event1.id", "123213123"),
                                                      verify_ent("Event 1 Desc", "event1.desc", "Uff"),
                                                      verify_ent("Events Count", "events.count", "3")]))

        vr = create_verification_request("checking order events v2", extraction_id, extraction_id)
        check_value(vr, "Event 1 ID", "event1.id", "123213123")
        check_value(vr, "Event 1 Desc contains", "event1.desc", "Order",
                    VerificationDetails.VerificationMethod.CONTAINS)
        compare_values(vr, "Event IDs", "event1.id", "event2.id")
        call(common_act.verifyEntities, vr)
