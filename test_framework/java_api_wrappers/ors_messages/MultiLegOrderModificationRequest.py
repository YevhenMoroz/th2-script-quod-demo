from datetime import datetime

from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class MultiLegOrderModificationRequest(JavaApiMessage):
    def __init__(self, data_set, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.MultiLegOrderModificationRequest.value, data_set=data_set)
        super().change_parameters(parameters)
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'MultiLegOrderModificationRequestBlock':
                {'LegOrderElements': {'LegOrderBlock': [{'LegNumber': 1,
                                                         'LegInstrID': "Uei8O2K3PXKyaP6jKe-CDA",
                                                         'LegPrice': 10},
                                                        {'LegNumber': 2, 'LegInstrID': "bNNcPIwlrClVbcZGtPJDkw",
                                                         'LegPrice': 2}]}},
            'OrdType': "LMT",
            'Price': 20,
            'TimeInForce': "DAY",
            'PositionEffect': "O",
            'OrdQty': '100',
            'OrdID': '*',
            'OrdCapacity': "A",
            'TransactTime': datetime.utcnow().isoformat(),
            'MaxPriceLevels': 1,
            'BookingType': "REG",
            'SettlCurrency': u"EUR",
            'RouteID': 24,
            'ExecutionPolicy': "D",
            'AccountGroupID': "CLIENT1",
            'WashBookAccountID': "DefaultWashBook",
            'PriceDelta': 0
        }

    def set_default(self):
        self.change_parameters(self.base_parameters)
