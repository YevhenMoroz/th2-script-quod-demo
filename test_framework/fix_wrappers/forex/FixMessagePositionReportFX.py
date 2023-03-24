from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixMessageRequestForPositions import FixMessageRequestForPositions


class FixMessagePositionReportFX(FixMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.PositionReport.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_params_from_reqeust(self, request: FixMessageRequestForPositions):
        base_parameters = {
            "PosReqID": request.get_parameter("PosReqID"),
            "Account": request.get_parameter("Account"),
            "Currency": request.get_parameter("Currency"),
            "Instrument": request.get_parameter("Instrument"),
            "PosMaintRepID": "*",
            "PosReqType": "0",
            "PosMaintRptID": "*",
            "SubscriptionRequestType": "1",
            "TotalNumPosReports": "*",
            "PosReqResult": "*",
            "SettlDate": "*",
            "PosReqStatus": "*",
            "PositionQty": "*",
            "PositionAmountData": "*",
            "LastPositEventType": "*",
            "LastPositUpdateEventID": "*",
            "NoParty": "*"
        }
        super().change_parameters(base_parameters)
