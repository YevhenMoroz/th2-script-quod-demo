from datetime import datetime, timezone
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class NewOrderMultiLeg(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.NewOrderMultiLeg.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'NewOrderMultiLegBlock': {
                'Side': 'Buy',
                'Price': "10",
                'QtyType': 'Units',
                'OrdType': 'Limit',
                'TimeInForce': 'Day',
                'PositionEffect': 'Open',
                'SettlCurrency': data_set.get_currency_by_name("currency_1"),
                'OrdCapacity': 'Agency',
                'TransactTime': (
                    tm(datetime.now(timezone.utc).isoformat()) + bd(n=2)
                )
                .date()
                .strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': "1",
                'ClientInstructionsOnly': 'No',
                'OrdQty': "100",
                'AccountGroupID': data_set.get_client_by_name("client_1"),
                'ExecutionPolicy': 'DMA',
                'ListingList': {
                    'ListingBlock': [
                        {'ListingID': data_set.get_listing_id_by_name("listing_1")}
                    ]
                },
                'InstrID': data_set.get_instrument_id_by_name("instrument_1"),
            },
        }
        super().change_parameters(base_parameters)
