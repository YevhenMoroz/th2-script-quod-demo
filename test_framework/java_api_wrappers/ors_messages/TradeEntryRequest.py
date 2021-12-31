from datetime import datetime, timedelta

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.java_api_wrappers.JavaApiDataSet import ORSMessages
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class TradeEntryRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessages.OrderSubmit.value)
        super().change_parameters(parameters)

    def set_default(self, ord_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'TradeEntryRequestBlock': {
                'OrdID': ord_id,
                'ExecPrice': "10.000000000",
                'ExecQty': "100.000000000",
                'TradeEntryTransType': 'NEW',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'LastMkt': 'XPAR',
                'TradeDate': (tm(datetime.utcnow().isoformat())).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'SettlDate': (tm(datetime.utcnow().isoformat()) + timedelta(days=2)).date().strftime(
                    '%Y-%m-%dT%H:%M:%S')
            }
        }
        super().change_parameters(base_parameters)

