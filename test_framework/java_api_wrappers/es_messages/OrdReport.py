from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.message_types import ESMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrdReport(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ESMessageType.OrdReport.value)
        super().change_parameters(parameters)

    def set_default(self):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            "Header": {
                "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            },
            "OrdReportBlock": {
                "LastVenueOrdID": "*",
                "SecondaryOrderID": "13",
                "ClOrdID": "*",
                "ReplySource": "Exchange",
                "TransactTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                "FreeNotes": "reportViaJavaApi",
                "Side": "Buy",
                "OrdQty": "100",
                "VenueExecID": basic_custom_actions.client_orderid(10),
                "CumQty": "0.0",
                "LeavesQty": "100.0",
                "AvgPrice": "0.0",
                "ExecType": "Open",
                "OrdType": "Limit",
                "ReplyReceivedTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S')
            }
        }
        super().change_parameters(base_parameters)

