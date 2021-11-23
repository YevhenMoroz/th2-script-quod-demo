from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle
from quod_qa.wrapper_test.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest


class FixMessageOrderCancelRequestOMS(FixMessageOrderCancelRequest):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__(new_order_single, parameters)

