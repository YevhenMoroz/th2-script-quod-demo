from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class NewOrderList(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.NewOrderList.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'NewOrderListBlock': {
                "NewOrderListElements": {
                    "NewOrderSingleBlock": [{
                        'Side': 'Buy',
                        'Price': "10",
                        'OrdType': 'Limit',
                        'TimeInForce': 'Day',
                        'OrdCapacity': 'Agency',
                        'OrdQty': "100",
                        'AccountGroupID': data_set.get_client_by_name("client_1"),
                        'ListingList': {'ListingBlock': [{'ListingID': data_set.get_listing_id_by_name("listing_1")}]},
                        'InstrID': data_set.get_instrument_id_by_name("instrument_1")
                    }, {
                        'Side': 'Sell',
                        'Price': "10",
                        'OrdType': 'Limit',
                        'TimeInForce': 'Day',
                        'OrdCapacity': 'Agency',
                        'OrdQty': "100",
                        'AccountGroupID': data_set.get_client_by_name("client_1"),
                        'ListingList': {'ListingBlock': [{'ListingID': data_set.get_listing_id_by_name("listing_1")}]},
                        'InstrID': data_set.get_instrument_id_by_name("instrument_1")
                    }]
                },
                'ListExecutionPolicy': 'Care',
                'ListTimeInForce': 'Day',
                'OrderListName': basic_custom_actions.client_orderid(9),
            }, 'CDOrdAssignInstructionsBlock': {
                'RecipientUserID': "JavaApiUser",
                'RecipientRoleID': 'Trader',
                'RecipientDeskID': '1',
            }}
        super().change_parameters(base_parameters)
