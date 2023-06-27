from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class QuoteRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=ORSMessageType.OrderQuoteRequest.value)
        super().change_parameters(parameters)
        self.data_set = data_set

    def set_default(self, qty="100", side=None, route_id=None) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "QuoteRequestBlock": {
                'QuoteReqList': {'QuoteReqBlock': [{
                    "OrdQty": qty,
                    "InstrID": self.data_set.get_instrument_id_by_name("instrument_1"),
                    "ListingID": self.data_set.get_listing_id_by_name("listing_1"),
                }]},
                "QuoteReqBatchID": f"QuoteReqBatchID-{basic_custom_actions.client_orderid(9)}",
            }}
        if side is not None:
            base_parameters["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["Side"] = side
        if route_id is not None:
            base_parameters["QuoteRequestBlock"]["RouteID"] = route_id
        super().change_parameters(base_parameters)
