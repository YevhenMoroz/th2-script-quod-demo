from test_framework.data_sets.message_types import QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class StopQuotingRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=QSMessageType.StopQuotingRequest.value)
        super().change_parameters(parameters)

    def set_default(self, listing_id, side=None, forced_cancel="Y") -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.QS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.QS',
            "StopQuotingRequestBlock": {
                "StopQuoteList": {
                    "StopQuoteBlock": [{
                        "ListingID": listing_id,
                        "ForcedCancel": forced_cancel}]}}
        }
        block = base_parameters['StopQuotingRequestBlock']['StopQuoteList']["StopQuoteBlock"][0]
        if side: block["Side"] = side
        super().change_parameters(base_parameters)
        return self
