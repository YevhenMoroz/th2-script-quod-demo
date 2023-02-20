from datetime import datetime, timezone

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.java_api_wrappers.ors_messages.FixOrderCancelRequest import FixOrderCancelRequest


class FixOrderCancelRequestOMS(FixOrderCancelRequest):
    def __init__(self, data_set: BaseDataSet, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)
        self.data_set = data_set

        self.base_parameters = {
            'SEND_SUBJECT': 'QUOD.ORS.FIX',
            'REPLY_SUBJECT': 'QUOD.FIX_REPLY.gtwquod4',
            'OrderCancelRequestBlock': {
                "ClOrdID": "cl_ord_id",
                "OrigClOrdID": "cl_ord_id",
                'TransactTime': (tm(datetime.now(timezone.utc).isoformat()) + bd(n=2)).date().strftime(
                    '%Y-%m-%dT%H:%M:%S'),
            }
        }

    def set_default_cancel(self, cl_ord_id):
        self.change_parameters(self.base_parameters)
        self.update_fields_in_component('OrderCancelRequestBlock',
                                        {'ClOrdID': cl_ord_id, 'OrigClOrdID': cl_ord_id})
        return self

