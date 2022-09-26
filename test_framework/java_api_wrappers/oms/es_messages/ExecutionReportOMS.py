from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.es_messages.ExecutionReport import ExecutionReport


class ExecutionReportOMS(ExecutionReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.FIXBUYTH2TEST.REPLY',
            'REPLY_SUBJECT': 'QUOD.FIXBUYTH2TEST.ES.REPLY',
            "Header": {"OnBehalfOf": {"OnBehalfOfCompID": "PARIS"},
                       "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                       "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                           '%Y-%m-%dT%H:%M:%S')},
            "ExecutionReportBlock": {"InstrumentBlock": data_set.get_java_api_instrument("instrument_1"),
                                     "ClOrdID": "*",
                                     "VenueExecID": basic_custom_actions.client_orderid(9),
                                     "LastVenueOrdID": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                                         '%Y-%m-%dT%H:%M:%S'),
                                     "OrdQty": "100.0",
                                     "Side": "Buy",
                                     "LastTradedQty": "100.0",
                                     "LastPx": "20.0",
                                     "TransactTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                                         '%Y-%m-%dT%H:%M:%S'),
                                     "OrdType": "Limit",
                                     "Price": "20.0",
                                     "Currency": "EUR",
                                     "ExecType": "Trade",
                                     "LastMkt": data_set.get_mic_by_name("mic_1"),
                                     "TimeInForce": "Day",
                                     "LeavesQty": "0.0",
                                     "CumQty": "100.0",
                                     "AvgPrice": "20.0"}
        }

    def set_default_trade(self, cl_ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('ExecutionReportBlock', {"ClOrdID": cl_ord_id})
        return self
