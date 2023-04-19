from copy import deepcopy
from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.es_messages.ExecutionReport import ExecutionReport
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields


class ExecutionReportOMS(ExecutionReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            'REPLY_SUBJECT': 'QUOD.BUYTH2TEST.ES.REPLY',
            "Header": {"OnBehalfOf": {"OnBehalfOfCompID": "PARIS"},
                       "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                       "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                           '%Y-%m-%dT%H:%M:%S')},
            "ExecutionReportBlock": {"InstrumentBlock": data_set.get_java_api_instrument("instrument_1"),
                                     "ClOrdID": "*",
                                     "VenueExecID": basic_custom_actions.client_orderid(9),
                                     "LastVenueOrdID": basic_custom_actions.client_orderid(15),
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
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('ExecutionReportBlock', {"ClOrdID": cl_ord_id})
        return self

    def set_default_new(self, cl_ord_id):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('ExecutionReportBlock', {"ClOrdID": cl_ord_id,
                                                                 "LastTradedQty": "0.0",
                                                                 "LastPx": "0.0",
                                                                 "OrdType": "Limit",
                                                                 "Price": "20.0",
                                                                 "ExecType": "Open",
                                                                 "TimeInForce": "Day",
                                                                 "LeavesQty": "100.0",
                                                                 "CumQty": "0.0",
                                                                 "AvgPrice": "0.0",
                                                                 })
        return self

    def set_default_cancel_unsolicited_execution(self, execution_report, last_venue_exec_id, venue_act_grp_name,
                                                 venue_ord_id, venue_exec_id):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('ExecutionReportBlock',
                                        {
                                            "ClOrdID": execution_report[JavaApiFields.ClOrdID.value],
                                            "OrdQty": execution_report[JavaApiFields.OrdQty.value],
                                            "LastTradedQty": execution_report[JavaApiFields.ExecQty.value],
                                            "LastPx": execution_report[JavaApiFields.Price.value],
                                            "TransactTime": (
                                                    tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                                                '%Y-%m-%dT%H:%M:%S'),
                                            "ExecType": "TradeCancel",
                                            "TimeInForce": "Day",
                                            "LeavesQty": execution_report[JavaApiFields.CumQty.value],
                                            "CumQty": execution_report[JavaApiFields.CumQty.value],
                                            "AvgPrice": execution_report[JavaApiFields.Price.value],
                                            'ExternalTransStatus': 'Open',
                                            JavaApiFields.VenueAccount.value:
                                                {JavaApiFields.VenueActGrpName.value: venue_act_grp_name},
                                            'VenueExecRefID': last_venue_exec_id,
                                            'VenueOrdID': venue_ord_id,
                                            'VenueExecID': venue_exec_id
                                        })
        return self

    def set_default_cancel(self, venue_exec_id, last_venue_ord_id, execution_report):
        self.change_parameters(deepcopy(self.base_parameters))
        self.update_fields_in_component('ExecutionReportBlock',
                                        {
                                            "ClOrdID": execution_report[JavaApiFields.OrdID.value],
                                            "OrdQty": execution_report[JavaApiFields.OrdQty.value],
                                            "TransactTime": (
                                                    tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime(
                                                '%Y-%m-%dT%H:%M:%S'),
                                            "ExecType": "TradeCancel",
                                            'VenueExecRefID': venue_exec_id,
                                            'LastVenueOrdID': last_venue_ord_id,
                                            'VenueExecID': basic_custom_actions.client_orderid(9)
                                        })
        return self

