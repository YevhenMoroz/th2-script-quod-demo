from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from stubs import Stubs
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.OrderSubmit import OrderSubmit


class OrderSubmitOMS(OrderSubmit):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'NewOrderSingleBlock': {
                'Side': 'Buy',
                'QtyType': 'Units',
                'OrdType': 'Market',
                'TimeInForce': 'Day',
                'PositionEffect': 'Open',
                'SettlCurrency': 'EUR',
                'OrdCapacity': 'Agency',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': "1",
                'ExecutionOnly': 'No',
                'ClientInstructionsOnly': 'No',
                'BookingType': 'RegularBooking',
                'OrdQty': "100",
                'AccountGroupID': data_set.get_client_by_name("client_1"),
                'ExecutionPolicy': 'DMA',
                'ListingList': {'ListingBlock': [{'ListingID': data_set.get_db_listing_by_name("listing_1")}]},
                'InstrID': data_set.get_db_instrument_by_name("instrument_1")
            }
        }

    def set_default_care_limit(self, recipient=Stubs.custom_config['qf_trading_fe_user'], role="HSD", desk="1"):
        params = {'CDOrdAssignInstructionsBlock': {'RecipientUserID': recipient,
                                                   'RecipientRoleID': role,
                                                   'RecipientDeskID': desk}}
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "20", 'ExecutionPolicy': 'Care'})
        self.add_tag(params)
        return self

    def set_default_dma_limit(self):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {"Price": '20', "OrdType": 'Limit'})
        return self

    def set_default_dma_market(self):
        self.change_parameters(self.base_parameters)
        return self

    def set_default_care_market(self, recipient=Stubs.custom_config['qf_trading_fe_user'], role="HSD", desk="1"):
        params = {'CDOrdAssignInstructionsBlock': {'RecipientUserID': recipient,
                                                   'RecipientRoleID': role,
                                                   'RecipientDeskID': desk}}
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {'ExecutionPolicy': 'Care'})
        self.add_tag(params)
        return self
