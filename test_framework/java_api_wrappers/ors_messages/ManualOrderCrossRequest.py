from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ManualOrderCrossRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.ManualOrderCrossRequest.value)
        super().change_parameters(parameters)

    def set_default(self, data_set, ord_id1, ord_id2, exec_price="5", exec_qty="100") -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'ManualOrderCrossRequestBlock': {
                'ManualOrderCrossTransType': 'New',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'ExecPrice': exec_price,
                'ExecQty': exec_qty,
                'ListingID': data_set.get_listing_id_by_name('listing_1'),
                'OrdID1': ord_id1,
                'OrdID2': ord_id2,
                'LastCapacity': 'Agency',
                'LastMkt': 'UBSG'
            }
        }
        super().change_parameters(base_parameters)
