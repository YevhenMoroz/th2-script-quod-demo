from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixPositionMaintenanceRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=PKSMessageType.FixPositionMaintenanceRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self):
        request_params = {
            "SEND_SUBJECT": "QUOD.PKS.FE",
            "REPLY_SUBJECT": "QUOD.POSIT.CLIENT1_1.EUR/USD",
            "PositionMaintenanceRequestBlock": {
                "InstrumentBlock": {
                    "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "ProductType": "CURRENCY",
                    "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot"),
                    "Tenor": self.get_data_set().get_tenor_by_name("tenor_spot")
                },
                "ClientAccountGroupID": "CLIENT1",
                "PosMaintAction": "DEL",
                "PosTransType": "ADJ",
                "ClientPosReqID": bca.client_orderid(9),
                "ClearingBusinessDate": "20230116",
                "PositionAmountDataList": {
                    "PositionAmountDataBlock": [
                        {
                            "PosAmtType": "BASE",
                            "PosAmt": "0",
                            "PositionCurrency": "USD",
                        },
                        {
                            "PosAmtType": "INIQ",
                            "PosAmt": "0",
                            "PositionCurrency": "USD",
                        },
                    ]

                }

            }
        }
        super().change_parameters(request_params)
        return self
