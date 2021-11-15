from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import Instrument
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleAlgo(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)
    #set_DMA_params
    def set_DMA(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "XPAR_CLIENT2",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': Instrument.BUI.value,
            'TimeInForce': '0',
            "TransactTime": '*',
            'SettlDate': '*',
            'ExDestination': "XPAR",
            'OrderCapacity': 'A',
            'NoParty': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
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
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.BUI.value,
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
            'ClOrdID': basic_custom_actions.client_orderid(9),
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
            'Price': 30,
            'OrdType': 2,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': Instrument.BUI.value,
            'OrderCapacity': 'A',
            'Currency': "EUR",
            'TargetStrategy': 1005,
            'ExDestination': 'XPAR',
            'QuodFlatParameters': {
                'NavigatorLimitPrice': '31',
                'NavGuard': '1',
                'NavigatorExecution': '1',
                'AllowedVenues': 'XPAR',
                'Waves': '5',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_MOO_Scaling(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.FR0010263202.value,
            "TargetStrategy": "1012",
            'QuodFlatParameters': {
                'MaxParticipation': '10',
                'PricePoint1Price': '28',
                'PricePoint1Participation': '12',
                'PricePoint2Price': '26',
                'PricePoint2Participation': '14',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_MOC_Scaling(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.FR0010263202.value,
            "TargetStrategy": "1015",
            'QuodFlatParameters': {
                'MaxParticipation': '10',
                'PricePoint1Price': '28',
                'PricePoint1Participation': '12',
                'PricePoint2Price': '26',
                'PricePoint2Participation': '14',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_Scaling(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': "CLIENT1",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '500000',
            'TimeInForce': '0',
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            'Instrument': Instrument.FR0010263202.value,
            'TargetStrategy': '2',
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10',
                'PricePoint1Price': '28',
                'PricePoint1Participation': '12',
                'PricePoint2Price': '26',
                'PricePoint2Participation': '14',
                'ExcludePricePoint2': '1'
            }
        }
        super().change_parameters(base_parameters)
        return self