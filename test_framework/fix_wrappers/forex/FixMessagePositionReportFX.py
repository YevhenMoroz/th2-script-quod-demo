from custom.verifier import Verifier
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessageRequestForPositions import FixMessageRequestForPositions


class FixMessagePositionReportFX(FixMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.PositionReport.value, data_set=data_set)
        super().change_parameters(parameters)
        self.verifier = Verifier()

    def set_params_from_reqeust(self, request: FixMessageRequestForPositions):
        base_parameters = {
            "PosReqID": request.get_parameter("PosReqID"),
            "Account": request.get_parameter("Account"),
            "Currency": request.get_parameter("Currency") if request.get_parameter("Currency") is not None else "*",
            "PosReqType": "0",
            "PosMaintRptID": "*",
            "SettlDate": "*",
            "PositionAmountData": "*",
            "LastPositEventType": "*",
            "LastPositUpdateEventID": "*",
            "TransactTime": "*",
            "Parties": "*",
            "Instrument": dict(SecurityType=request.get_parameter("Instrument")["SecurityType"],
                               Symbol=request.get_parameter("Instrument")["Symbol"],
                               SecurityID=request.get_parameter("Instrument")["Symbol"],
                               SecurityIDSource="8",
                               SecurityExchange="*"
                               )
        }
        super().change_parameters(base_parameters)

        return self

    def set_params_for_all(self, request: FixMessageRequestForPositions):
        base_parameters = {
            "PosReqID": request.get_parameter("PosReqID"),
            "Account": request.get_parameter("Account"),
            "Currency": "*",
            "PosReqType": "0",
            "PosMaintRptID": "*",
            "SettlDate": "*",
            "PositionAmountData": "*",
            "LastPositEventType": "*",
            "LastPositUpdateEventID": "*",
            "TransactTime": "*",
            "Parties": "*",
            "Instrument": "*"
        }
        super().change_parameters(base_parameters)

        return self
