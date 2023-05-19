from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class AssignInstrumentRequest(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.AssignInstrumentRequest.value)
        super().change_parameters(parameters)

    def set_default(self, listing_ids: list, instrument_id, order_id) -> None:
        listings_list = []
        for listing_id in listing_ids:
            listings_list.append({'ListingID': listing_id})
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "AssignInstrumentRequestBlock":
                {'ListingList': {'ListingBlock': listings_list},
                 'OrdID': order_id,
                 'InstrID': instrument_id
                 }}
        super().change_parameters(base_parameters)
