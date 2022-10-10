from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class RequestForFXPositions(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=PKSMessageType.RequestForFXPositions.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self):
        params_for_request = {
            "SEND_SUBJECT": "QUOD.CLIENT1_1.POSIT",
            "REPLY_SUBJECT": "QUOD.POSIT.CLIENT1_1",
            "RequestForFXPositionsBlock": {
                "PosReqType": "Positions",
                # "AccountID": self.get_data_set().get_client_by_name("client_mm_1"),
                "AccountID": "CLIENT1",
                "Currency": self.get_data_set().get_currency_by_name("currency_usd"),
                "SubscriptionRequestType": "Subscribe",
            }
        }
        super().change_parameters(params_for_request)

    def change_subject(self, subject):
        self.change_parameter("SEND_SUBJECT", f"QUOD.{subject}.POSIT")
        self.change_parameter("REPLY_SUBJECT", f"QUOD.POSIT.{subject}")

    def set_unsubscribe(self):
        self.update_fields_in_component("RequestForFXPositionsBlock", {"SubscriptionRequestType": "Unsubscribe"})
        return self
