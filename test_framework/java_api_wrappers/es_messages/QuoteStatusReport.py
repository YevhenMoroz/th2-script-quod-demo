from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ESMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class QuoteStatusReport(JavaApiMessage):

    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__(message_type=ESMessageType.QuoteStatusReport.value)
        super().change_parameters(parameters)
        self.data_set = data_set

    def set_default(self, quote_id, quote_status):
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ES.BUYTH2TEST.REPLY',
            "Header": {
                "MsgTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                "CreationTime": (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
            },
            "QuoteStatusReportBlock": {
                "QuoteMsgID": quote_id,
                "QuoteStatus": quote_status,
            }
        }
        super().change_parameters(base_parameters)
        return self
