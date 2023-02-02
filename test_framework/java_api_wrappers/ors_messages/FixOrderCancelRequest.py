from datetime import datetime, timezone

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class FixOrderCancelRequest(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.FixOrderCancelRequest.value)
        super().change_parameters(parameters)

    def set_default(self, cl_ord_id) -> None:
        base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FIX',
            'OrderCancelRequestBlock': {
                "ClOrdID": cl_ord_id,
                "OrigClOrdID": cl_ord_id,
                'TransactTime': (tm(datetime.now(timezone.utc).isoformat()) + bd(n=2)).date().strftime(
                    '%Y-%m-%dT%H:%M:%S'),
            }
        }
        super().change_parameters(base_parameters)
