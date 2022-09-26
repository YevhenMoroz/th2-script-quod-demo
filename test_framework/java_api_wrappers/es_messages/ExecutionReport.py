from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ESMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


# TODO finish writing
class ExecutionReport(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ESMessageType.ExecutionReport.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYGTW.REPLY',
            "Header": {"OnBehalfOf": {"OnBehalfOfCompID": "PARIS"},
                       "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                       "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                           '%Y-%m-%dT%H:%M:%S')},
            "ExecutionReportBlock": {"InstrumentBlock": data_set.get_java_api_instrument("instrument_1"),
                                     "ClOrdID": "*",
                                     "VenueExecID": "*",
                                     "LastVenueOrdID": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                                         '%Y-%m-%dT%H:%M:%S'),
                                     "OrdQty": "100.0",
                                     "Side": "Buy",
                                     "LastTradedQty": "100.0",
                                     "LastPx": "10.0",
                                     "TransactTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                                         '%Y-%m-%dT%H:%M:%S'),
                                     "OrdType": "Limit",
                                     "Price": "10.0",
                                     "Currency": data_set.get_currency_by_name("currency_1"),
                                     "ExecType": "Trade",
                                     "LastMkt": data_set.get_mic_by_name("mic_1"),
                                     "TimeInForce": "Day",
                                     "LeavesQty": "0.0",
                                     "CumQty": "100.0",
                                     "AvgPrice": "10.0"}
        }
        super().change_parameters(base_parameters)
