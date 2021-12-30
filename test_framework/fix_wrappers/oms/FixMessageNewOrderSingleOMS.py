from datetime import datetime

from custom import basic_custom_actions
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleOMS(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        "Account": "CLIENT1",
        'ClOrdID': basic_custom_actions.client_orderid(9),
        "Side": "1",
        'OrderQtyData': {'OrderQty': '100'},
        "TimeInForce": "0",
        "Instrument": Instrument.FR0010436584.value,
        "TransactTime": datetime.utcnow().isoformat(),
        "OrderCapacity": "A",
        "Currency": "EUR",
        "ExDestination": "XPAR"
    }

    def set_default_dma_limit(self, instr: Instrument = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "2", "HandlInst": "1", "Price": "20"})
        if instr:
            self.change_parameters({"Instrument": instr.value})
        return self

    def set_default_care_limit(self, instr: Instrument = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "2", "HandlInst": "3", "Price": "20"})
        if instr:
            self.change_parameters({"Instrument": instr.value})
        return self

    def set_default_dma_market(self, instr: Instrument = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "1", "HandlInst": "1"})
        if instr:
            self.change_parameters({"Instrument": instr.value})
        return self

    def set_default_care_market(self, instr: Instrument = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "1", "HandlInst": "3"})
        if instr:
            self.change_parameters({"Instrument": instr.value})
        return self

    def set_default_dma_limit_eurex(self, instr: Instrument = None):
        self.change_parameters(self.base_parameters)
        self.change_parameters({"OrdType": "2", "HandlInst": "2", "Price": "20","ExDestination": "XEUR"})
        if instr:
            self.change_parameters({"Instrument": instr.value})
        return self