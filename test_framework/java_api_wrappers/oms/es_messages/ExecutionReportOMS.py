from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.es_messages.ExecutionReport import ExecutionReport


class ExecutionReportOMS(ExecutionReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.FIXBUYTH2TEST.REPLY',
            "Header": {"OnBehalfOf": {"OnBehalfOfCompID": "PARIS"},
                       "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                       "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                           '%Y-%m-%dT%H:%M:%S')},
            "ExecutionReportBlock": {"InstrumentBlock": {"InstrSymbol": "FR0010436584_EUR",
                                                         "SecurityID": "FR0010436584",
                                                         "SecurityIDSource": "ISI",
                                                         "InstrType": "Equity",
                                                         "SecurityExchange": "XPAR"},
                                     "ClOrdID": "*",
                                     "VenueExecID":  "*",
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
                                     "Currency": "EUR",
                                     "ExecType": "Trade",
                                     "LastMkt": "XPAR",
                                     "TimeInForce": "Day",
                                     "LeavesQty": "0.0",
                                     "CumQty": "100.0",
                                     "AvgPrice": "10.0"}
        }

    def set_default(self):
        self.change_parameters(self.base_parameters)
        return self
