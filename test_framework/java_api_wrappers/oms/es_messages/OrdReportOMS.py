from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.es_messages.OrdReport import OrdReport


class OrdReportOMS(OrdReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.FIXBUYTH2TEST.REPLY',
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
                "Side": "Sell",
                "OrdQty": "100",
                "Price": "10",
                "VenueExecID": "1",
                "CumQty": "0.0",
                "LeavesQty": "100.0",
                "AvgPrice": "0.0",
                "ExecType": "Open",
                "OrdType": "Limit",
                "ReplyReceivedTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            }
        }

    def set_default_open(self, ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrdReportBlock',
                                        {"LastVenueOrdID": ord_id, "Price": "20", 'ClOrdID': ord_id})

    def set_default_eliminated(self, ord_id, price):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrdReportBlock', {"LastVenueOrdID": ord_id, "Price": price, 'ClOrdID': ord_id,
                                                           'ExecType': 'Eliminated'})
        return self
