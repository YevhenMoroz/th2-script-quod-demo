from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.java_api_wrappers.JavaApiDataSet import ORSMessages, ListingID
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class ManualOrderCrossRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessages.ManualOrderCrossRequest.value)
        super().change_parameters(parameters)

    def set_default(self, ord_id1, ord_id2, exec_price="5", exec_qty="100") -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'ManualOrderCrossRequestBlock': {
                'ManualOrderCrossTransType': 'New',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'ExecPrice': exec_price,
                'ExecQty': exec_qty,
                'ListingID': ListingID.PAR_VETO.value,
                'OrdID1': ord_id1,
                'OrdID2': ord_id2,
                'LastCapacity': 'Agency',
                'LastMkt': 'UBSG'
            }
        }
        super().change_parameters(base_parameters)
