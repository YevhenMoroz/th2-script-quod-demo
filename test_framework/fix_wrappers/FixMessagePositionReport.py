from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.data_sets.message_types import FIXMessageType
from custom import basic_custom_actions as bca


class FixMessagePositionReport(FixMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.PositionReport.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            "PosReqID": bca.client_orderid(9),
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
            "Account": "*",
            "Currency": "EUR",
            "Instrument": {
                "SecurityType": "FXSPOT",
                "Symbol": "EUR/USD",
            },
            "NoParty": "*"
        }
        super().change_parameters(base_parameters)
