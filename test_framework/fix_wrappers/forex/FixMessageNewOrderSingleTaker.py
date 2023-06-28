from datetime import datetime
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleTaker(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(data_set=data_set)
        super().change_parameters(parameters)

    def set_default_SOR(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol=self.get_data_set().get_symbol_by_name("symbol_1"),                      # 55
            SecurityType=self.get_data_set().get_security_type_by_name("fx_spot"),          # 167
        )
        base_parameters = {
            "ClOrdID": bca.client_orderid(9),                                               # 11
            "Account": self.get_data_set().get_client_by_name("client_5"),                  # 1
            "HandlInst": "2",                                                               # 21
            "Side": "1",                                                                    # 54
            "OrderQty": "1000000",                                                          # 38
            "TimeInForce": "0",                                                             # 59
            "OrdType": "2",                                                                 # 40
            "TransactTime": datetime.utcnow().isoformat(),                                  # 60
            "Price": "1.18999",                                                             # 44
            "Currency": self.get_data_set().get_currency_by_name("currency_eur"),           # 15
            "Instrument": instrument,
            "TargetStrategy": "1008",                                                       # 847
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),               # 64
            "SettlType": self.get_data_set().get_settle_type_by_name("spot"),               # 63
            "NoStrategyParameters": [                                                       # 957
                {
                    'StrategyParameterName': 'AllowedVenues',                               # 958
                    'StrategyParameterType': '14',                                          # 959
                    'StrategyParameterValue': 'MS/CITI'                                     # 960
                }
            ]
        }
        super().change_parameters(base_parameters)
        return self

    def set_default_mo(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol=self.get_data_set().get_symbol_by_name("symbol_1"),                      # 55
            SecurityType=self.get_data_set().get_security_type_by_name("fx_spot")           # 167
        )
        base_parameters = {
            "ClOrdID": bca.client_orderid(9),                                                # 11
            "Account": self.get_data_set().get_client_by_name("client_5"),                   # 1
            "HandlInst": "2",                                                                # 21
            "Side": "1",                                                                     # 54
            "OrderQty": "1000000",                                                           # 38
            "TimeInForce": "0",                                                              # 59
            "OrdType": "2",                                                                  # 40
            "TransactTime": datetime.utcnow().isoformat(),                                   # 60
            "Price": "1.18999",                                                              # 44
            "Currency": self.get_data_set().get_currency_by_name("currency_eur"),            # 15
            "Instrument": instrument,
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),                # 64
            "SettlType": self.get_data_set().get_settle_type_by_name("spot"),                # 63
            "ExDestination": "CITI-SW"                                                       # 100

        }
        super().change_parameters(base_parameters)
        return self

    def set_default_care(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol=self.get_data_set().get_symbol_by_name("symbol_1"),                      # 55
            SecurityType=self.get_data_set().get_security_type_by_name("fx_spot")           # 167
        )
        base_parameters = {
            "ClOrdID": bca.client_orderid(9),                                                # 11
            "Account": self.get_data_set().get_client_by_name("client_5"),                   # 1
            "HandlInst": "3",                                                                # 21
            "Side": "1",                                                                     # 54
            "OrderQty": "5000000",                                                           # 38
            "TimeInForce": "0",                                                              # 59
            "OrdType": "2",                                                                  # 40
            "TransactTime": datetime.utcnow().isoformat(),                                   # 60
            "Price": "1.18999",                                                              # 44
            "Currency": self.get_data_set().get_currency_by_name("currency_eur"),            # 15
            "Instrument": instrument,
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),                # 64
            "SettlType": self.get_data_set().get_settle_type_by_name("spot"),                # 63
            # "ExDestination": "CITI-SW"                                                       # 100

        }
        super().change_parameters(base_parameters)
        return self