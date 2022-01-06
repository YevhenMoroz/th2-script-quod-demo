from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.java_api_wrappers.JavaApiDataSet import ListingID, InstrID
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderSubmit(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderSubmit.value)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'NewOrderSingleBlock': {
                'Side': 'Buy',
                'Price': "10",
                'QtyType': 'Units',
                'OrdType': 'Limit',
                'TimeInForce': 'Day',
                'PositionEffect': 'Open',
                'SettlCurrency': 'EUR',
                'OrdCapacity': 'Agency',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': "1",
                'ClientInstructionsOnly': 'No',
                'OrdQty': "100",
                'AccountGroupID': 'CLIENT1',
                'ExecutionPolicy': 'DMA',
                'ListingList': {'ListingBlock': [{'ListingID': ListingID.PAR_VETO.value}]},
                'InstrID': InstrID.PAR.value
            }
        }
        super().change_parameters(base_parameters)
