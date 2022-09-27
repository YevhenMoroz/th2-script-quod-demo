from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.OrderSubmit import OrderSubmit


class OrderSubmitOMS(OrderSubmit):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set
        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYGTW.REPLY',
            'REPLY_SUBJECT': 'QUOD.BUYGTW.ES.REPLY',
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
                "OrdQty": "100.000000000",
                "Price": "20.000000000",
                "VenueExecID": basic_custom_actions.client_orderid(9),
                "CumQty": "0.000000000",
                "LeavesQty": "100.000000000",
                "AvgPrice": "20.000000000",
                "ExecType": "Open",
                "OrdType": "Limit",
                "TimeInForce": "Day",
                "ExDestination": data_set.get_mic_by_name("mic_1"),
                "ReplyReceivedTime": datetime.utcnow().isoformat(),
                "VenueAccount": {"VenueActGrpName": data_set.get_venue_client_account("client_1_venue_1")},
            }
        }

