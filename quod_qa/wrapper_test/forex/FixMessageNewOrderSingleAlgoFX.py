from datetime import datetime
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle



class FixMessageNewOrderSingleAlgoFX(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_default_SOR(self) -> FixMessageNewOrderSingle:
        instrument = dict(
            Symbol='EUR/USD',                                    #55
            SecurityType='FXSPOT',                               #167
        )
        base_parameters = {
            "ClOrdID": bca.client_orderid(9),                    #11
            "Account": "TH2_Taker",                              #1
            "HandlInst": "2",                                    #21
            "Side": "1",                                         #54
            "OrderQty": "1000000",                               #38
            "TimeInForce": "0",                                  #59
            "OrdType": "2",                                      #40
            "TransactTime": datetime.utcnow().isoformat(),       #60
            "Price": "1.18999",                                  #44
            "Currency": "EUR",                                   #15
            "Instrument": instrument,
            "TargetStrategy": "1008",                            #847
            "SettlDate": spo(),                                  #64
            "SettlType": '0'                                     #63
            # "NoStrategyParameters":[                             #957
            #     {
            #         'StrategyParameterName': 'AllowedVenues',    #958
            #         'StrategyParameterType': '14',               #959
            #         'StrategyParameterValue': 'EBS-CITI/DB'      #960
            #     }
            # ]
        }
        super().change_parameters(base_parameters)
        return self