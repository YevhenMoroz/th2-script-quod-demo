from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest


class FixMessageOrderCancelReplaceRequestOMS(FixMessageOrderCancelReplaceRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.parameters = parameters
        self.change_parameters(parameters)

    base_parameters = {
        "Account": "CLIENT1",
        "Side": "1",
        'OrderQtyData': {'OrderQty': '100'},
        "OrdType": "2",
        "HandlInst": "3",
        "ClOrdID": "*",
        "OrigClOrdID": "*",
        "Instrument": Instrument.FR0010436584.value,
        "TransactTime": datetime.utcnow().isoformat(),
    }

    def set_default(self):
        self.change_parameters(self.base_parameters)
        return self