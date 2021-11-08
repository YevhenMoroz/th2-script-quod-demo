from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleAlgo(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_TWAP(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "1",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.FR0010436584.value,
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

    def set_TWAP_Navigator(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT1",
            "HandlInst": "0",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "110",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.FR0000062788.value,
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
                'NavigatorExecution': '1',
                'NavGuard': '0',
                'NavigatorLimitPrice': '100',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV(self) -> FixMessageNewOrderSingle:

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
            "Instrument": Instrument.FR0010436584.value,
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_Navigator_Guard(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 10000000,
            'TimeInForce': 0,
            'Price': 117,
            'OrdType': 2,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': Instrument.FR0000062788.value,
            'OrderCapacity': 'A',
            'Currency': "GBX",
            'TargetStrategy': 1005,
            'ExDestination': 'XPAR',
            'QuodFlatParameters': {
                'NavigatorPercentage': '100',
                'NavigatorExecution': '1',
                'NavigatorInitialSweepTime': '5',
                'NavGuard': '0',
                'AllowedVenues': 'XLON'
            }
        }
        super().change_parameters(base_parameters)
        return self