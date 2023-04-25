from datetime import datetime, timedelta

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.FixNewOrderList import FixNewOrderList
from test_framework.java_api_wrappers.ors_messages.NewOrderList import NewOrderList


class FixNewOrderListOMS(FixNewOrderList):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        instrument_1 = self.data_set.get_java_api_instrument("instrument_1")
        self.base_parameters = {
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

    def set_default_order_list(self):
        self.change_parameters(self.base_parameters)
        return self

    def add_simple_order_to_list(self):
        parameters = self.base_parameters['ListOrdGrp']['NoOrders'].append(
            self.base_parameters['ListOrdGrp']['NoOrders'][0])
        self.change_parameters(parameters)
        return self
