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
    def set_DMA_params(self, needNoParty:bool=True) -> FixMessageNewOrderSingle:
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
            'OrderCapacity': 'A'
        }
        if needNoParty == True:
            base_parameters['NoParty'] = '*'
            # 'Origin': '*'

        super().change_parameters(base_parameters)
        return self

    # set_DMA_ME_params
    def set_DMA_ME_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "CLIENT2",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': Instrument.BUI.value,
            'TimeInForce': '0',
            "TransactTime": datetime.utcnow().isoformat(),
            'ExDestination': "XMCE",
            'OrderCapacity': 'A'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_RB_params(self) -> FixMessageNewOrderSingle:
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
            'Parties': '*',
            'QtyType': '0',
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_params(self) -> FixMessageNewOrderSingle:
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
            'ExDestination': self.get_data_set().get_mic_by_name('mic_1'),
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1005"
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_Redburn_params(self) -> FixMessageNewOrderSingle:
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
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_auction_params(self) -> FixMessageNewOrderSingle:
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
            'ExDestination': self.get_data_set().get_mic_by_name('mic_1'),
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
                "ParticipateInOpeningAuctions": "Y",
                "ParticipateInClosingAuctions": "Y"
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TWAP_Intraday_auction_params(self) -> FixMessageNewOrderSingle:
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
            'ExDestination': self.get_data_set().get_mic_by_name('mic_1'),
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1005",
            'QuodFlatParameters': {
                "ParticipateInIntradayAuctions": "Y",
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_VWAP_auction_params(self) -> FixMessageNewOrderSingle:
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
            'ExDestination': self.get_data_set().get_mic_by_name('mic_1'),
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_1"),
            "TargetStrategy": "1",
            'QuodFlatParameters': {
                "ParticipateInOpeningAuctions": "Y",
                "ParticipateInClosingAuctions": "Y"
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


    def set_VWAP_buy_back_params(self):
        self.set_VWAP_params()
        self.update_fields_in_component('QuodFlatParameters', dict(Custom='Passive'))
        return self

    def set_VWAP_Redburn_params(self) -> FixMessageNewOrderSingle:
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
            "TargetStrategy": "2",
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'PercentageVolume',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '0.1'
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_Redburn_params(self) -> FixMessageNewOrderSingle:
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
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_Auctions_params(self) -> FixMessageNewOrderSingle:
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
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10',
                "ParticipateInOpeningAuctions": "Y",
                "ParticipateInClosingAuctions": "Y"
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_MOO_Auction_params(self) -> FixMessageNewOrderSingle:
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
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10',
                "ParticipateInOpeningAuctions": "Y",
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_MOC_Auction_params(self) -> FixMessageNewOrderSingle:
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
            "TargetStrategy": "2",
            'QuodFlatParameters': {
                'MaxPercentageVolume': '10',
                "ParticipateInClosingAuctions": "Y"
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
        super().change_parameters(base_parameters)
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

    def set_MOC_AtLast_params(self) -> FixMessageNewOrderSingle:
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
                'ExcludePricePoint2': '1',
                'AtLast': '1'
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

    def set_MOO_Would_params(self) -> FixMessageNewOrderSingle:
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
                'WouldInAuction': '1',
                'ExcludePricePoint2': '1',
                'TriggerPriceRed': '29'
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
                'NumberOfLevels': '10'
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
                'NumberOfLevels': '10'
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
                'NumberOfLevels': '10',
                'ExcludePricePoint2': '1'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_Minimum_Participation_params(self) -> FixMessageNewOrderSingle:
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
                'MinParticipation': '9'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_POV_min_value_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_2'),
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
                    'StrategyParameterName': 'PercentageVolume',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '0.3'
                },
                {
                    'StrategyParameterName': 'ChildMinValue',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '150'
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

    def set_Multilisting_with_algopolicy_params(self) -> FixMessageNewOrderSingle:
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
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_Single_1',
        }
        super().change_parameters(base_parameters)
        return self

    def set_Multilisting_RB_params(self) -> FixMessageNewOrderSingle:
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
            'TargetStrategy': '1008',
            'QuodFlatParameters': {
                'AvailableVenues': 'True',
                'AllowMissingPrimary': 'True'
            }
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

    def set_Single_listed_LitSOR_with_Iceberg_and_Peg_params(self):
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
            'TargetStrategy': '1008',
            "DisplayInstruction": {
                'DisplayQty': '15000'
            },
            'PegInstructions': {
                'PegOffsetValue': '0.2',
                'PegPriceType': '1',
                'PegOffsetType': '0'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TIF_params(self):
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
            'TargetStrategy': '1003'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Auction_Child_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": 'CLIENT1',
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_21'),
            'TimeInForce': '2',
            "TransactTime": '*',
            'ExDestination': 'XAMS',
            'OrderCapacity': 'A',
        }
        super().change_parameters(base_parameters)
        return self

    def set_MPDark_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'ClientAlgoPolicyID': 'QA_Auto_MPDark',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Dark_Child_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'ChildOrderID': '*',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Dark_Child_Kepler_SORPING_params(self) -> FixMessageNewOrderSingle:
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
            'ChildOrderID': '*',
            'misc5': '*',
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
            "IClOrdIdAO": "*"
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_after_RFQ_params(self):
        base_parameters = {
            "Account": 'KEPLER',
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': 1,
            'OrderQty': 3000000,
            'OrdType': "D",
            'Price': 20,
            'Side': 1,
            'Instrument': "*",
            'TimeInForce': 0,
            "TransactTime": '*',
            'ExDestination': 'LISX',
            'OrderCapacity': 'A',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'AlgoCst01': 'firm-up',
            'AlgoCst03': '*',
            'QuoteID': '*',
            'ChildOrderID': '*',
            'misc5': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_SynthMinQty_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'ClientAlgoPolicyID': 'QA_Auto_SOR_PassivePrioPrimary',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'MinQty': '100'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_ChildMinQty_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_LitDark_Iceberg_Kepler_params(self):
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
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_ME_Y',
            "DisplayInstruction": {
                'DisplayQty': '500'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_of_LitDark_Iceberg_Kepler_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "XPAR_CLIENT2",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_9'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "XPAR",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_Iceberg_Kepler_params_specific_tags(self):
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
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1004',
            'IClOrdIdCO': 'OD_5fgfDXg-00',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'IClOrdIdTO': '19864',
            'AlgoCst01': 'KEPLER06',
            'AlgoCst02': 'KEPLER07',
            'AlgoCst03': 'KEPLER10',
            'ExDestination': 'QDL1',
            'ClientAlgoPolicyID': 'QA_Auto_ICEBERG',
            "DisplayInstruction": {
                'DisplayQty': '500'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_of_Iceberg_Kepler_params_specific_tags(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "KEPLER",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "QDL1",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'IClOrdIdCO': 'OD_5fgfDXg-00',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'IClOrdIdTO': '19864',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_SORPING_Iceberg_Kepler_params_with_PartyInfo(self):
        base_parameters = {
            'ClOrdID': '*',
            'HandlInst': "2",
            'NoParty': [
                {
                    'PartyID': 'TestINITIATOR-UTI',
                    'PartyIDSource': 'D',
                    'PartyRole': '55'
                }
            ],
            'Account': "KEPLER",
            'ExDestination': 'QDL1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'Side': '1',
            'TransactTime': datetime.utcnow().isoformat(),
            'OrderQty': '500000',
            'OrdType': "2",
            'Price': "20",
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'TimeInForce': "0",
            'OrderCapacity': 'A',
            'TargetStrategy': '1004',
            'ClientAlgoPolicyID': 'QA_Auto_ICEBERG',
            "DisplayInstruction": {
                'DisplayQty': '500'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_of_SORPING_Iceberg_Kepler_params_with_PartyInfo(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "KEPLER",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "QDL1",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'misc5': '*',
            'NoTradingSessions': '*',
            'NoParty': [
                {
                    'PartyID': 'TestINITIATOR-UTI',
                    'PartyIDSource': 'D',
                    'PartyRole': '55'
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_LitDark_Iceberg_Kepler_params_with_PartyInfo(self):
        base_parameters = {
            'ClOrdID': '*',
            'HandlInst': "2",
            'NoParty': [
                {
                    'PartyID': 'TestClientID',
                    'PartyIDSource': 'D',
                    'PartyRole': '3'
                }
            ],
            'Account': "KEPLER",
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_9'),
            'Side': '1',
            'TransactTime': datetime.utcnow().isoformat(),
            'OrderQty': '500000',
            'OrdType': "2",
            'Price': "20",
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'TimeInForce': "0",
            'OrderCapacity': 'A',
            'TargetStrategy': '1011',
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_3',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            "DisplayInstruction": {
                'DisplayQty': '500'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_of_LitDark_Iceberg_Kepler_params_with_PartyInfo(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "KEPLER",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "QDL1",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'misc5': '*',
            'NoTradingSessions': '*',
            'NoParty': [
                {
                    'PartyID': 'TestINITIATOR-UTI',
                    'PartyIDSource': 'D',
                    'PartyRole': '55'
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_Iceberg_Kepler_params(self):
        base_parameters = {
            'ClOrdID': '*',
            'HandlInst': "2",
            'Account': "KEPLER",
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_9'),
            'Side': '1',
            'TransactTime': datetime.utcnow().isoformat(),
            'OrderQty': '500000',
            'OrdType': "2",
            'Price': "20",
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'TimeInForce': "0",
            'OrderCapacity': 'A',
            'TargetStrategy': '1004',
            'ClientAlgoPolicyID': 'QA_Auto_ICEBERG',
            'ExDestination': 'XPAR',
            "DisplayInstruction": {
                'DisplayQty': '500'
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_of_Iceberg_Kepler_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "KEPLER",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_9'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "XPAR",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Kepler_params(self):
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
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'ExDestination': 'QDL1',
            'IClOrdIdCO': 'OD_5fgfDXg-00',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'IClOrdIdTO': '19864'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_Kepler_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "KEPLER",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_8'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "QDL1",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'IClOrdIdCO': 'OD_5fgfDXg-00',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'IClOrdIdTO': '19864',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_SORPING_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_1',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Child_of_SORPING_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'ShortCode': '17536',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_Multiple_Emulation_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_13'),
            'TargetStrategy': '1011',
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_ME_Y',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536'
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Child_of_Multiple_Emulation_Kepler_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": 'KEPLER',
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '11',
            'Side': '2',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_13'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': 'QDL6',
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_Multilisting_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            "Price": "30",
            "Currency": self.get_data_set().get_currency_by_name('currency_1'),
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_8"),
            'TargetStrategy': '1008',
            'NoParty': [
                {
                    'PartyID': '12345678',
                    'PartyIDSource': 'D',
                    'PartyRole': '12'
                }
            ],
            'ComplianceID': 'FX5',
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_4',
            'IClOrdIdAO': 'OD_5fgfDXg-00',
            'ShortCode': '17536'

        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_Child_of_Multilisting_Kepler_params(self) -> FixMessageNewOrderSingle:
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
            'ShortCode': '17536',
            'NoParty': '*',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_Synthetic_TIF_Kepler_params(self):
        base_parameters = {
            'ClOrdID': '*',
            'HandlInst': "2",
            'Account': "KEPLER",
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_17'),
            'Side': '1',
            'TransactTime': datetime.utcnow().isoformat(),
            'OrderQty': '500000',
            'OrdType': "2",
            'Price': "20",
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'TimeInForce': "1",
            'OrderCapacity': 'A',
            'TargetStrategy': '1003',
            'ExDestination': 'QDL11',
        }
        super().change_parameters(base_parameters)
        return self

    def set_DMA_child_of_Synthetic_TIF_Kepler_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            "Account": "KEPLER",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_17'),
            'TimeInForce': '0',
            "TransactTime": '*',
            'ExDestination': "QDL11",
            'OrderCapacity': 'A',
            'ChildOrderID': '*',
            'misc5': '*',
            'NoTradingSessions': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def set_LitDark_params(self) -> FixMessageNewOrderSingle:
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
            'TargetStrategy': '1011',
            'ClientAlgoPolicyID': 'InternalQuodQa_SORPING',
            'NoStrategyParameters': [
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_Block_params(self):
        base_parameters = {
            'Account': "CLIENT2",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '1000',
            'TimeInForce': "0",
            'Price': "20",
            'OrdType': "2",
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_2'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1019',
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'ReleaseMode',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LastTradedQty'
                },
                {
                    'StrategyParameterName': 'ModifyFactor',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': '1'
                }

            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_Stop_params(self):
        base_parameters = {
            'Account': "CLIENT2",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '1000',
            'TimeInForce': "0",
            'StopPx': "20",
            'OrdType': 3,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_2'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1001'
        }
        super().change_parameters(base_parameters)
        return self

    def set_Pegged_params(self):
        base_parameters = {
            'Account': "CLIENT2",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '1000',
            'Price': '20',
            'TimeInForce': "0",
            'OrdType': '2',
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_2'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1009',
            'PegInstructions': {
                'PegOffsetValue': '1',
                'PegPriceType': '1',
                'PegOffsetType': '0',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_Multilisting_with_Peg_params(self) -> FixMessageNewOrderSingle:
        base_parameters = {
            'Account': self.get_data_set().get_account_by_name('account_28'),
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
            'Instrument': self.get_data_set().get_fix_instrument_by_name("instrument_36"),
            'TargetStrategy': '1008',
            'ClientAlgoPolicyID': 'QA_Auto_SORPING_Spray_1',
            'PegInstructions': {
                'PegOffsetValue': '0.2',
                'PegPriceType': '1',
                'PegOffsetType': '0',
            }
        }
        super().change_parameters(base_parameters)
        return self

    def set_TrailingStop_params(self):
        base_parameters = {
            'Account': "CLIENT2",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '1000',
            'TimeInForce': "0",
            'OrdType': 1,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_2'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1006',
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'TriggerPriceType',
                    'StrategyParameterType': '13',
                    'StrategyParameterValue': 'LastTrade'
                },
                {
                    'StrategyParameterName': 'OffsetValue',
                    'StrategyParameterType': '13',
                    'StrategyParameterValue': 'true'
                },
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_Triggering_params(self):
        base_parameters = {
            'Account': "CLIENT2",
            'ClOrdID': '*',
            'HandlInst': "2",
            'Side': '1',
            'OrderQty': '1000',
            'TimeInForce': "0",
            'OrdType': 2,
            'Price': 1,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': self.get_data_set().get_fix_instrument_by_name('instrument_2'),
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'TargetStrategy': '1020',
            'TriggeringInstruction': {
                'TriggerType': 4,
                'TriggerAction': 1,
            },
        }
        super().change_parameters(base_parameters)
        return self
