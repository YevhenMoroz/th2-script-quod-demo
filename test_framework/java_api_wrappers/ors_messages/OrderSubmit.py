from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderSubmit(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.OrderSubmit.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'NewOrderSingleBlock': {
                'Side': 'Buy',
                'Price': "10",
                'QtyType': 'Units',
                'OrdType': 'Limit',
                'TimeInForce': 'Day',
                'PositionEffect': 'Open',
                'SettlCurrency': data_set.get_currency_by_name("currency_1"),
                'OrdCapacity': 'Agency',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': "1",
                'ClientInstructionsOnly': 'No',
                'OrdQty': "100",
                'AccountGroupID': data_set.get_client_by_name("client1"),
                'ExecutionPolicy': 'DMA',
                'ListingList': {'ListingBlock': [{'ListingID': data_set.get_db_listing_by_name("instrument_1")}]},
                'InstrID': data_set.get_db_instrument_by_name("listing_1")
            }
        }
        super().change_parameters(base_parameters)
