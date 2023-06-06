from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixRequestForPositionsFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=PKSMessageType.FixRequestForPositions.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_params(self):
        quote_request_params = {
            "SEND_SUBJECT": "QUOD.PKS.REQUEST",
            "REPLY_SUBJECT": "QUOD.PKS.REPLY",
            "RequestForPositionsBlock": {
                "ClientPosReqID": bca.client_orderid(9),
                "InstrumentBlock": {
                    "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot"),
                },
                "PosReqType": "Positions",
                "SubscriptionRequestType": "Subscribe",
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_1"),
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),

            }
        }
        super().change_parameters(quote_request_params)
        return self

    def change_client(self, client):
        params = self.get_parameters()
        params["RequestForPositionsBlock"]["ClientAccountGroupID"] = client
        return self

    def change_instrument(self, instrument, currency):
        params = self.get_parameters()
        params["RequestForPositionsBlock"]["InstrumentBlock"] = instrument
        params["RequestForPositionsBlock"]["Currency"] = currency
        return self

    def unsubscribe(self):
        self.update_fields_in_component("RequestForPositionsBlock", {"SubscriptionRequestType": "Unsubscribe"})
        return self
