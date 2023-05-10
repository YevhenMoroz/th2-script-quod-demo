from datetime import datetime

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixMessageRequestForPositions import FixMessageRequestForPositions
from test_framework.fix_wrappers.FixMessageRequestForPositionsAck import FixMessageRequestForPositionsAck


class FixMessageRequestForPositionsAckFX(FixMessageRequestForPositionsAck):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(parameters, data_set=data_set)

    def set_params_from_reqeust(self, request: FixMessageRequestForPositions):
        base_parameters = {
            "PosReqID": request.get_parameter("PosReqID"),
            "PosMaintRptID": "*",
            "PosReqType": "0",
            "SubscriptionRequestType": "1",
            "TotalNumPosReports": "*",
            "PosReqResult": "Valid",
            "PosReqStatus": "Completed",
            "Account": request.get_parameter("Account"),
            "Currency": request.get_parameter("Currency"),
            "Instrument": request.get_parameter("Instrument"),
        }
        # "NoParty": [{
        #     "PartyID": "CLIENT1_1",
        #     "PartyIDSource": "POS",
        #     "PartyRole": "D",
        #
        # }]
        super().change_parameters(base_parameters)
        return self

    def set_params_for_none(self, request: FixMessageRequestForPositions):
        base_parameters = {
            "PosReqID": request.get_parameter("PosReqID"),
            "PosMaintRptID": "*",
            "PosReqType": "0",
            "SubscriptionRequestType": "1",
            "TotalNumPosReports": "0",
            "PosReqResult": "2",
            "PosReqStatus": "0",
            "Account": request.get_parameter("Account"),
            "Currency": request.get_parameter("Currency"),
            "Instrument": request.get_parameter("Instrument"),
        }
        # "NoParty": [{
        #     "PartyID": "CLIENT1_1",
        #     "PartyIDSource": "POS",
        #     "PartyRole": "D",
        #
        # }]
        super().change_parameters(base_parameters)
        return self

    def set_unsubscribe(self):
        self.change_parameter("SubscriptionRequestType", "2")
        return self
