from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class QuoteRequestActionRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=ORSMessageType.QuoteRequestActionRequest.value, data_set=data_set)
        super().change_parameters(parameters)
        self.action_id = bca.client_orderid(10)

    def set_default_params(self, quote_req_id):
        params_for_request = {
            "SEND_SUBJECT": "QUOD.ORS.FE",
            "REPLY_SUBJECT": "QUOD.FE.ORS",
            "QuoteRequestActionRequestBlock": {
                "QuoteRequestID": str(quote_req_id),
                "QuoteReqAction": None,
                "AssigneeUserID": "ostronov",
                "AssigneeRoleID": "HSD",
                "ActionID": f"{quote_req_id}{self.action_id}"
            }
        }
        super().change_parameters(params_for_request)
        return self

    def set_action_assign(self):
        self.update_fields_in_component("QuoteRequestActionRequestBlock", {"QuoteReqAction": "ASG"})

    def set_action_estimate(self):
        self.update_fields_in_component("QuoteRequestActionRequestBlock", {"QuoteReqAction": "EST"})

    def set_action_reject(self):
        self.update_fields_in_component("QuoteRequestActionRequestBlock", {"QuoteReqAction": "Reject"})
