from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.NewOrderList import NewOrderList


class NewOrderListOMS(NewOrderList):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
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
                },'CDOrdAssignInstructionsBlock': {
                    'RecipientUserID': "JavaApiUser",
                    'RecipientRoleID': 'Trader',
                    'RecipientDeskID': '1',
                }}

    def set_default_order_list(self):
        self.change_parameters(self.base_parameters)
        return self

    def add_simple_order_to_list(self):
        parameters = self.base_parameters['NewOrderListBlock']['NewOrderListElements']['NewOrderSingleBlock'].append(
            self.base_parameters['NewOrderListBlock']['NewOrderListElements']['NewOrderSingleBlock'][0])
        self.change_parameters(parameters)
        return self
