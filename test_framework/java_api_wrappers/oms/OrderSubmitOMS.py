from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from stubs import Stubs
from test_framework.java_api_wrappers.JavaApiDataSet import Listing, InstrID
from test_framework.java_api_wrappers.ors_messages.OrderSubmit import OrderSubmit


class OrderSubmitOMS(OrderSubmit):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
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
            'AccountGroupID': 'CLIENT1',
            'ExecutionPolicy': 'DMA',
            'ListingList': Listing.PAR_VETO.value,
            'InstrID': InstrID.PAR.value
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

    def set_default_care_market(self):
        params = {'CDOrdAssignInstructionsBlock': {'RecipientUserID': Stubs.custom_config['qf_trading_fe_user'],
                                                   'RecipientRoleID': 'HSD',
                                                   'RecipientDeskID': '1'}}
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {'ExecutionPolicy': 'Care'})
        self.add_tag(params)
        return self
