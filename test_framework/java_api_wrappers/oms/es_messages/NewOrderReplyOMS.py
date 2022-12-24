from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.es_messages.NewOrderReply import NewOrderReply


class NewOrderReplyOMS(NewOrderReply):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            'REPLY_SUBJECT': 'QUOD.BUYTH2TEST.ES.REPLY',
            "Header": {
                "MsgTime": datetime.utcnow().isoformat(),
                "CreationTime": datetime.utcnow().isoformat()},
            "NewOrderReplyBlock": {
                "InstrumentBlock": data_set.get_java_api_instrument("instrument_1"),
                "LastVenueOrdID": basic_custom_actions.client_orderid(9),
                "ClOrdID": "*",
                "ReplySource": "Exchange",
                "TransactTime": datetime.utcnow().isoformat(),
                "Side": "Buy",
                "OrdQty": "100.0",
                "Price": "20.0",
                "VenueExecID": basic_custom_actions.client_orderid(9),
                "CumQty": "0.0",
                "LeavesQty": "100.0",
                "AvgPrice": "20.0",
                "ExecType": "Open",
                "OrdType": "Market",
                "TimeInForce": "Day",
                "ExDestination": data_set.get_mic_by_name("mic_1"),
                "ReplyReceivedTime": datetime.utcnow().isoformat(),
                "VenueAccount": {"VenueActGrpName": data_set.get_venue_client_names_by_name("client_1_venue_1")},
            }
        }

    def set_default_dma_limit(self, cl_ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderReplyBlock', {"Price": '20', "OrdType": 'Limit',
                                                               "ClOrdID": cl_ord_id})
        return self

    def set_unsolicited_dma_limit(self):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('NewOrderReplyBlock',
                                        {"Price": '20', "OrdType": 'Limit', "UnsolicitedOrder": "Yes",
                                         "ClOrdID": basic_custom_actions.client_orderid(9)})
        return self
