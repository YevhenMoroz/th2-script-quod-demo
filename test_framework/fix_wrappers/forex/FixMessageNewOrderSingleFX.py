from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from custom import basic_custom_actions as bca


class FixMessageNewOrderSingleFX(FixMessageNewOrderSingle):
    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(parameters)
    
    def set_default(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol="EUR/USD",                                    # 55
            SecurityType="FXSPOT",                               # 167
            Product="4"                                          # 460
        )
        base_parameters = {
            "ClOrdID": bca.client_orderid(9),                    # 11
            "Account": "CLIENT1",                                # 1
            "HandlInst": "2",                                    # 21
            "Side": "1",                                         # 54
            "OrderQty": "1000000",                               # 38
            "TimeInForce": "4",                                  # 59
            "OrdType": "2",                                      # 40
            "TransactTime": datetime.utcnow().isoformat(),       # 60
            "Price": "1.18999",                                  # 44
            "Currency": "EUR",                                   # 15
            "Instrument": instrument,
            "SettlDate": spo(),                                  # 64
            "SettlType": "0",                                    # 63

        }
        super().change_parameters(base_parameters)
        return self