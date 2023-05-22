from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ExecutePricedOrderRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=QSMessageType.ExecutePricedOrderRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self, ord_id):
        params_for_request = {
            "SEND_SUBJECT": "QUOD.PRICING.2.FE",
            "REPLY_SUBJECT": "QUOD.FE.PRICING.2",
            "ExecutePricedOrderRequestBlock": {
                "OrdID": ord_id}}
        super().change_parameters(params_for_request)
        return self
