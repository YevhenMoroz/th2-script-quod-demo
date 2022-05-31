from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.DataSet import Instrument
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleAlgo(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(data_set=data_set)
        super().change_parameters(parameters)

    # set_DMA_params
    def set_DMA_params(self) -> FixMessageNewOrderSingle:
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
            'NoParty': '*',
            'Origin': '2'
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': 'CLIENT2',
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            'Currency': "EUR",
            'ExDestination': "XPAR",
            "Instrument": Instrument.BUI.value,
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_VWAP_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1",
            'QuodFlatParameters': {
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': "CLIENT2",
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            'Currency': "EUR",
            'ExDestination': "XPAR",
            "Instrument": Instrument.BUI.value,
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_Navigator_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": Instrument.BUI.value,
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
                'NavigatorExecution': '1',
                'NavGuard': '0',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_VWAP_Navigator_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": Instrument.BUI.value,
            "TargetStrategy": "1",
            'QuodFlatParameters': {
                'NavigatorExecution': '1',
                'NavGuard': '0',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_Navigator_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10',
                'NavigatorExecution': '1',
                'NavGuard': '0'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_Navigator_Guard_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            # 'Account': "CLIENT1",
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 10000000,
            'TimeInForce': 0,
            'Price': 30,
            'OrdType': 2,
            'TransactTime': datetime.utcnow().isoformat(),
            # 'Instrument': Instrument.BUI.value,
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            'OrderCapacity': 'A',
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'TargetStrategy': 1005,
            # 'ExDestination': 'XPAR',
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            'QuodFlatParameters': {
                'NavigatorLimitPrice': '31',
                'NavGuard': '1',
                'NavigatorExecution': '1',
                'AllowedVenues': 'XPAR',
                'Waves': '5',
            }
        }
        return self

    def set_MOO_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1012",
            'QuodFlatParameters': {
                'WouldInAuction': '0',
                'ExcludePricePoint2': '1'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_MOC_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1015",
            'QuodFlatParameters': {
                'WouldInAuction': '0',
                'ExcludePricePoint2': '1'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_MOE_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name("account_1"),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            'Currency': self.get_data_set().get_currency_by_name("currency_1"),
            'ExDestination': self.get_data_set().get_mic_by_name("mic_1"),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1014",
            'QuodFlatParameters': {
                'WouldInAuction': '0',
                'ExcludePricePoint2': '1'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_MOO_Scaling_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": self.get_data_set().get_account_by_name('account_1'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            "ExDestination": self.get_data_set().get_mic_by_name('mic_1'),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
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

    def set_MOC_Scaling_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": self.get_data_set().get_account_by_name('account_1'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "500000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            "ExDestination": self.get_data_set().get_mic_by_name('mic_1'),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
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

    def set_POV_Scaling_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_1'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '500000',
            'TimeInForce': '0',
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            "ExDestination": self.get_data_set().get_mic_by_name('mic_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
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

    def set_Multilisting_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_1'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '500000',
            'TimeInForce': '0',
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "30",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            'TargetStrategy': '1008',
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'AvailableVenues',
                    'StrategyParameterType': '13',
                    'StrategyParameterValue': 'true'
                },
                {
                    'StrategyParameterName': 'AllowMissingPrimary',
                    'StrategyParameterType': '13',
                    'StrategyParameterValue': 'true'
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_MPDark_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_9'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '500000',
            'TimeInForce': '0',
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_6'),
            'TargetStrategy': '1010',
            'ClientAlgoPolicyID': 'QA_MPDark2',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Dark_Child_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": 'KEPLER',
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
            'ExDestination': 'BATD',
            'OrderCapacity': 'A',
            'ShortCode': '17536',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ChildOrderID': '*'
        }
        super().change_parameters(base_parameters)
        return self
