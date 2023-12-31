from copy import deepcopy
from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleOMS(FixMessageNewOrderSingle):

    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            "Account": data_set.get_client_by_name("client_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "Side": "1",
            'OrderQtyData': {'OrderQty': '100'},
            "TimeInForce": "0",
            "Instrument": data_set.get_fix_instrument_by_name("instrument_1"),
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Currency": data_set.get_currency_by_name("currency_1"),
            "ExDestination": data_set.get_mic_by_name("mic_1")
        }

    def set_default_dma_limit(self, instr: str = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "2", "HandlInst": "1", "Price": "20"})
        if instr:
            self.change_parameters({"Instrument": self.data_set.get_fix_instrument_by_name(instr)})
        return self

    def set_default_care_limit(self, instr: str = None, account: str = None):
        self.change_parameters(deepcopy(self.base_parameters))
        self.change_parameters({"OrdType": "2", "HandlInst": "3", "Price": "20"})
        if instr:
            self.change_parameters({"Instrument": self.data_set.get_fix_instrument_by_name(instr)})
        if account:
            self.change_parameters({"Account": self.data_set.get_client_by_name(account)})
        return self

    def set_default_dma_market(self, instr: str = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "1", "HandlInst": "1"})
        if instr:
            self.change_parameters({"Instrument": self.data_set.get_fix_instrument_by_name(instr)})
        return self

    def set_default_care_market(self, instr: str = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "1", "HandlInst": "3"})
        if instr:
            self.change_parameters({"Instrument": self.data_set.get_fix_instrument_by_name(instr)})
        return self

    def set_default_iceberg(self, instr: str = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({'HandlInst': "2",
                                "OrdType": "2",
                                'Price': "20",
                                'TargetStrategy': '1004',
                                "DisplayInstruction": {
                                    'DisplayQty': '100'}})
        if instr:
            self.change_parameters({"Instrument": self.data_set.get_fix_instrument_by_name(instr)})
        return self

    def set_fix42_dma_limit(self):
        self.change_parameters(self.base_parameters)
        instr = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.change_parameters({"OrdType": "2", "HandlInst": "1", "Price": "20", "OrderQty": "100",
                                "Symbol": instr["Symbol"], "SecurityID": instr["SecurityID"],
                                "IDSource": instr["SecurityIDSource"], "SecurityExchange": instr["SecurityExchange"]})
        self.remove_parameters(["Instrument","OrderCapacity","OrderQtyData"])
        return self

    def set_fix42_care_limit(self):
        self.change_parameters(self.base_parameters)
        instr = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.change_parameters({"OrdType": "2", "HandlInst": "3", "Price": "20", "OrderQty": "100",
                                "Symbol": instr["Symbol"], "SecurityID": instr["SecurityID"],
                                "IDSource": instr["SecurityIDSource"], "SecurityExchange": instr["SecurityExchange"]})
        self.remove_parameters(["Instrument","OrderCapacity","OrderQtyData"])
        return self
