from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class RequestForOverdueRetailPositions(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=PKSMessageType.RequestForOverdueRetailPositions.value)
        super().change_parameters(parameters)

    def set_default(self, subscription_request_type, pos_req_type) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.PKS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.PKS',
            "RequestForOverdueRetailPositionsBlock": {
                'SubscriptionRequestType': subscription_request_type,
                'PosReqType': pos_req_type
            }}
        super().change_parameters(base_parameters)