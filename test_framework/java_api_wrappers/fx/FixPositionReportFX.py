from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.fx.FixRequestForPositionsFX import FixRequestForPositionsFX


class FixPositionReportFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=PKSMessageType.FixPositionReport.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            "PositionReportBlock": {}}
        super().change_parameters(base_parameters)

    def set_params_from_request(self, request: FixRequestForPositionsFX):
        params = request.get_parameters()["RequestForPositionsBlock"]
        base_params = {
            "PositionReportBlock": {
                "ClientPosReqID": params["ClientPosReqID"],
                "ClientAccountGroupID":  params["ClientAccountGroupID"],
                "Currency": params["Currency"] if params["Currency"] is not None else "*",
                "PosReqType": "POS",
                "PositionAmountDataList": "*",
                "InstrumentBlock": "*",
                "SettlDate": "*",
                "LastPositEventType": "*",
                "LastPositUpdateEventID": "*",
                "TransactTime": "*",
                "PartiesList": "*",
                "PosMaintRepID": "*",
            }
        }
        super().change_parameters(base_params)
        return self
