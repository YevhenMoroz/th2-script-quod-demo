from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class RequestForPositions(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=PKSMessageType.RequestForPositions.value)
        super().change_parameters(parameters)

    def set_default(self, subscription_request_type, pos_req_type, account_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.PKS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.PKS',
            "RequestForPositionsBlock": {
                'SubscriptionRequestType': subscription_request_type,
                'PosReqType': pos_req_type,
                'AccountID': account_id
            }}
        super().change_parameters(base_parameters)
