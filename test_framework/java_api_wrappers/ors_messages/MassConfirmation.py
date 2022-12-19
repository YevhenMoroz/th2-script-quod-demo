from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from datetime import datetime


class MassConfirmation(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.MassConfirmation.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.ALLOC.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            "MassConfirmationBlock": {
                'ConfirmationList': {'ConfirmationBlock': [{
                    "ConfirmationID": "0",
                    "AllocInstructionID": "*",
                    "AllocAccountID": data_set.get_account_by_name('client_pt_1_acc_1'),
                    "InstrID": data_set.get_instrument_id_by_name("instrument_1"),
                    "ConfirmTransType": "NEW",
                    "ConfirmType": "CON",
                    "TradeDate": datetime.utcnow().isoformat()
                }]}}}
        super().change_parameters(base_parameters)
