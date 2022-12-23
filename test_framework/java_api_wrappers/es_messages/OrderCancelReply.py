from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ESMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class OrderCancelReply(JavaApiMessage):
    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ESMessageType.OrderCancelReply.value)
        super().change_parameters(parameters)

    def set_default(self, data_set: BaseDataSet, cl_ord_id, ord_venue_id):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            'REPLY_SUBJECT': 'QUOD.BUYTH2TEST.ES.REPLY',
            "Header": {
                "MsgTime": datetime.utcnow().isoformat(),
                "CreationTime": datetime.utcnow().isoformat()},
            "OrderCancelReplyBlock": {
                "InstrumentBlock": data_set.get_java_api_instrument("instrument_1"),
                "LastVenueOrdID": ord_venue_id,
                "ClOrdID": cl_ord_id,
                "ReplySource": "Exchange",
                "TransactTime": datetime.utcnow().isoformat(),
                "Side": "Buy",
                "OrdQty": "100.000000000",
                "Price": "20.000000000",
                "VenueExecID": basic_custom_actions.client_orderid(9),
                "CumQty": "0.000000000",
                "LeavesQty": "100.000000000",
                "AvgPrice": "20.000000000",
                "ExecType": "CXL",
                "OrdType": "Limit",
                "TimeInForce": "Day",
                "ExDestination": data_set.get_mic_by_name("mic_1"),
                "ReplyReceivedTime": datetime.utcnow().isoformat(),
                "VenueAccount": {"VenueActGrpName": data_set.get_venue_client_names_by_name("client_1_venue_1")},
            }
        }
        super().change_parameters(base_parameters)
        return self
