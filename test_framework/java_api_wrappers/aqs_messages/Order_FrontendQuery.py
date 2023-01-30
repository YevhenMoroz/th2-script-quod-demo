from test_framework.data_sets.message_types import AQSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class Order_FrontendQuery(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=AQSMessageType.FrontendQuery.value)
        self.change_parameters(parameters)

    def set_default(self, order_id, store_procedure):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.AQS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.AQS',
            'FrontendQueryBlock': {
                'ParameterList': {'ParameterBlock':
                    [{
                        'StringParameterValue': order_id
                    }]},
                'StoredProcName': store_procedure
            }
        }
        return self.change_parameters(base_parameters)
