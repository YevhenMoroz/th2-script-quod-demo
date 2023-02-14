from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.es_messages.OrdReport import OrdReport


class OrdReportOMS(OrdReport):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            'REPLY_SUBJECT': 'QUOD.BUYTH2TEST.ES.REPLY',
            "Header": {
                "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            },
            "OrdReportBlock": {
                "InstrumentBlock": data_set.get_java_api_instrument("instrument_1"),
                "LastVenueOrdID": "*",
                "ClOrdID": "*",
                "ReplySource": "Exchange",
                "TransactTime": datetime.utcnow().isoformat(),
                "Side": "Buy",
                "OrdQty": "100.000000000",
                "Price": "20.000000000",
                "VenueExecID": bca.client_orderid(9),
                "CumQty": "0.000000000",
                "LeavesQty": "100.000000000",
                "AvgPrice": "20.000000000",
                "ExecType": "Open",
                "OrdType": "Limit",
                "TimeInForce": "Day",
                "ExDestination": data_set.get_mic_by_name("mic_1"),
                "ReplyReceivedTime": datetime.utcnow().isoformat(),
                "VenueAccount": {"VenueActGrpName": data_set.get_venue_client_names_by_name("client_1_venue_1")},
            }
        }

    def set_default_open(self, ord_id, venue_ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrdReportBlock',
                                        {"LastVenueOrdID": venue_ord_id, 'ClOrdID': ord_id})
        return self

    def set_default_eliminated(self, ord_id, price):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrdReportBlock', {"LastVenueOrdID": ord_id, "Price": price, 'ClOrdID': ord_id,
                                                           'ExecType': 'Eliminated'})
        return self
