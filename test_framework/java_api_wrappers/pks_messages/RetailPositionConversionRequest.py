from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class RetailPositionConversionRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=PKSMessageType.RetailPositionConversionRequest.value)
        super().change_parameters(parameters)

    def set_default(self, instr_id, account_id, date) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.PKS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.PKS',
            "RetailPositionConversionRequestBlock": {
                'AccountID': account_id,
                'InstrID': instr_id,
                'PositionType': 'N',
                'PosValidity': 'DEL',
                'PosGoodTillDate': date

            }}
        super().change_parameters(base_parameters)
