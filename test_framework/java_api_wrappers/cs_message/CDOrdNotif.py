from test_framework.data_sets.message_types import CSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class CDOrdNotif(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=CSMessageType.CDOrdNotif.value)
        self.change_parameters(parameters)

    def set_default(self):
        base_parameters = {}
        return self.change_parameters(base_parameters)
