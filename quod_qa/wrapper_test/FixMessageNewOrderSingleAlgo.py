from datetime import datetime

from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.Instrument import Instrument


class FixMessageNewOrderSingleAlgo(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_default_TWAP(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT1",
            "HandlInst": "0",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.FR0010436584,
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
                'ParticipateInOpeningAuctions': 'Y',
                'ParticipateInClosingAuctions': 'Y',
                'MaxParticipationOpen': '10',
                'MaxParticipationClose': '10',
                'SaveForClosePercentage': '80'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_POV(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol='FR0010436584',
            SecurityID='FR0010436584',
            SecurityIDSource='4',
            SecurityExchange='XPAR'
        )
        base_parameters = {
            "Account": "CLIENT1",
            "HandlInst": "0",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": instrument,
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10'
            }
        }
        super().change_parameters(base_parameters)
        return self
