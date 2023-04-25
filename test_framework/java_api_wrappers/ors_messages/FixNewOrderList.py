from datetime import datetime, timedelta

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType, QSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class FixNewOrderList(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.FixNewOrderList.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet) -> None:
        instrument_1 = self.data_set.get_java_api_instrument("instrument_1")
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FIX',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'NewOrderListBlock': {
                "ListID": basic_custom_actions.client_orderid(9),
                "NewOrderListElements": {
                    "NewOrderSingleBlock": [{
                        "ClOrdID": basic_custom_actions.client_orderid(9),
                        'ExecutionPolicy': 'Care',
                        'Side': 'Buy',
                        'Price': "10",
                        'OrdType': 'Limit',
                        'TimeInForce': 'Day',
                        'OrdCapacity': 'Agency',
                        'OrdQty': "100",
                        'ClientAccountGroupID': data_set.get_client_by_name("client_pt_1"),
                        "InstrumentBlock": instrument_1
                    }, {
                        "ClOrdID": basic_custom_actions.client_orderid(9),
                        'ExecutionPolicy': 'Care',
                        'Side': 'Sell',
                        'Price': "10",
                        'OrdType': 'Limit',
                        'TimeInForce': 'Day',
                        'OrdCapacity': 'Agency',
                        'OrdQty': "100",
                        'ClientAccountGroupID': data_set.get_client_by_name("client_pt_1"),
                        "InstrumentBlock": instrument_1
                    }]
                }
            }}
        super().change_parameters(base_parameters)
