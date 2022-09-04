from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.FixNewOrderSingle import FixNewOrderSingle


class FixNewOrderSingleOMS(FixNewOrderSingle):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FIX',
            'REPLY_SUBJECT': 'QUOD.FIX_REPLY.gtwquod4',
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
                'ClientAccountGroupID': data_set.get_client_by_name("client_1"),
                'ExecutionPolicy': 'DMA',
                "InstrumentBlock": {"InstrSymbol": "FR0010436584_EUR",
                                    "SecurityID": "FR0010436584",
                                    "SecurityIDSource": "ISIN",
                                    "InstrType": "Equity"},
                "ClOrdID": basic_custom_actions.client_orderid(9),
            }
        }

    def set_default_care_limit(self):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock',
                                        {"OrdType": 'Limit', "Price": "20", 'ExecutionPolicy': 'Care'})
        return self

    def set_default_dma_limit(self):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {"Price": '20', "OrdType": 'Limit'})
        return self

    def set_default_dma_market(self):
        self.change_parameters(self.base_parameters)
        return self

    def set_default_care_market(self):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderSingleBlock', {'ExecutionPolicy': 'Care'})
        return self
