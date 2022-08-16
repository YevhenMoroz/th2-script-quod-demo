from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from custom import basic_custom_actions as bca


class FixMessageNewOrderSingleFX(FixMessageNewOrderSingle):
    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(parameters, data_set=data_set)

    def set_default(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol=self.get_data_set().get_symbol_by_name("symbol_1"),                      # 55
            SecurityType=self.get_data_set().get_security_type_by_name("fx_spot"),          # 167
            Product="4"                                                                     # 460
        )
        base_parameters = {
            "ClOrdID": bca.client_orderid(9),                                               # 11
            "Account": self.get_data_set().get_client_by_name("client_mm_1"),               # 1
            "HandlInst": "2",                                                               # 21
            "Side": "1",                                                                    # 54
            "OrderQty": "1000000",                                                          # 38
            "TimeInForce": "4",                                                             # 59
            "OrdType": "2",                                                                 # 40
            "TransactTime": datetime.utcnow().isoformat(),                                  # 60
            "Price": "1.18999",                                                             # 44
            "Currency": self.get_data_set().get_currency_by_name("currency_eur"),           # 15
            "Instrument": instrument,
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),               # 64
            "SettlType": self.get_data_set().get_settle_type_by_name("spot"),               # 63

        }
        super().change_parameters(base_parameters)
        return self
