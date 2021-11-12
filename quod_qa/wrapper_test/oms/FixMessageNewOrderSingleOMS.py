from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleOMS(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_default_DMA(self, instr:Instrument = None):
        base_parameters = {
            "Account": "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            'OrderQtyData': {'OrderQty': '100'},
            "TimeInForce": "0",
            "OrdType": "2",
            "Instrument": instr.value if instr is not None else Instrument.FR0010436584.value,
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR"
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_CO(self):
        base_parameters = {
        }