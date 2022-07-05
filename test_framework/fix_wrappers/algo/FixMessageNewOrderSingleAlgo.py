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
            # 'Origin': '*'
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

    def set_POV_min_value_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_1'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            "HandlInst": "2",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            'Currency': self.get_data_set().get_currency_by_name('currency_1'),
            'ExDestination': self.get_data_set().get_mic_by_name('mic_1'),
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_2"),
            "TargetStrategy": "2",
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'Aggressivity',
                    'StrategyParameterType': '1',
                    'StrategyParameterValue': '1'
                },
                {
                    'StrategyParameterName': 'PercentageVolume',
                    'StrategyParameterType': '11',
                    'StrategyParameterValue': '10'
                },
                {
                    'StrategyParameterName': 'ChildMinValue',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '10'
                }
            ]
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
                },
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_Multilisting_spraying_params(self) -> FixMessageNewOrderSingle:
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
                },
                {
                    'StrategyParameterName': 'PostMode',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'Spraying'
                },
                {
                    'StrategyParameterName': 'VenueWeights',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'TRQX=7/PARIS=3'
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_Iceberg_params(self):
        base_parameters = {
            'Account': "CLIENT1",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '30000',
            'TimeInForce': "0",
            'Price': "20",
            'OrdType': "2",
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_2'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1004',
            "DisplayInstruction": {
                'DisplayQty': '15000'
            }
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
            'ShortCode': '17536',
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
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_6'),
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

    def set_SynthMinQty_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_9'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '500000',
            'TimeInForce': '0',
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "11",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TargetStrategy': '1008',
            'MinQty': '100'
        }
        super().change_parameters(base_parameters)
        return self

    def set_SynthMinQty_params_with_strategy(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_9'),
            'ClOrdID': basic_custom_actions.client_orderid(9),
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '500000',
            'TimeInForce': '0',
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "11",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TargetStrategy': '1008',
            'ClientAlgoPolicyID': 'QA_SORPING_2',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'MinQty': '100'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_ChildMinQty_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": 'KEPLER',
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '11',
            'Side': '2',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': 'QDL1',
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
        }
        super().change_parameters(base_parameters)
        return self

    def set_RFQ_params(self):
        base_parameters = {
            # 'Account': self.get_data_set().get_account_by_name('account_9'),
            'Account': "KEPLER",
            'ClOrdID': "*",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'ExecInst': 'A',
            'HandlInst': '1',
            'OrderQty': '500000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'TimeInForce': '0',
            'TransactTime': "*",
            "OrderCapacity": "A",
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_6'),
            "ExDestination": "LISX",
            "AlgoCst01": "ioi",
            "QtyType": "0",
        }
        super().change_parameters(base_parameters)
        return self

    def set_SORPING_Iceberg_params(self):
        base_parameters = {
            'Account': "KEPLER",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '500000',
            'TimeInForce': "0",
            'Price': "20",
            'OrdType': "2",
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_9'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1011',
            'ClientAlgoPolicyID': 'QA_SORPING',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            "DisplayInstruction": {
                'DisplayQty': '500'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_SORPING_params(self) -> FixMessageNewOrderSingle:
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
            "Price": "11",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TargetStrategy': '1011',
            'ClientAlgoPolicyID': 'QA_SORPING_1',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Child_of_SORPING_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": 'KEPLER',
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '11',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': 'QDL1',
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536'
        }
        super().change_parameters(base_parameters)
        return self
