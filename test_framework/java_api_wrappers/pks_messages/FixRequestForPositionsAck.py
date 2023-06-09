from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.fx.FixRequestForPositionsFX import FixRequestForPositionsFX


class FixRequestForPositionsAck(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=PKSMessageType.FixRequestForPositionsAck.value)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            "RequestForPositionsAckBlock": {}}
        super().change_parameters(base_parameters)

    def set_params_from_request_sub(self, reqeust: FixRequestForPositionsFX):
        base_params = {
            "MaxErrorLevel": "I",
            "RequestForPositionsAckBlock": {
                "TotalNumPosReports": "*",
                "ClientPosReqID": reqeust.get_parameters()["RequestForPositionsBlock"]["ClientPosReqID"],
                "SettlDate": self.parse_settle_date(reqeust.get_parameters()["RequestForPositionsBlock"]["SettlDate"]),
                "PosReqResult": "*",
                "SubscriptionRequestType": "SUB",
                "ClientAccountGroupID": reqeust.get_parameters()["RequestForPositionsBlock"]["ClientAccountGroupID"],
                "Currency": reqeust.get_parameters()["RequestForPositionsBlock"]["Currency"],
                "InstrumentBlock": {
                    "InstrType": "SPO",
                    "InstrSymbol": reqeust.get_parameters()["RequestForPositionsBlock"]["InstrumentBlock"][
                        "InstrSymbol"],
                },
                "PosMaintRepID": "*",
                "PosReqType": "POS",
                "PosReqStatus": "CPL",

            }
        }
        super().change_parameters(base_params)

    def parse_settle_date(self, settle_date):
        return settle_date[:11] + "12:00"
