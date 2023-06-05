from datetime import datetime

from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest


class FixMessageOrderCancelRequestFX(FixMessageOrderCancelRequest):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_from_trade(self, order_id):
        base_parameters = {
            "OrigClOrdID": order_id,
            "ClOrdID": "*",
        }
        super().change_parameters(base_parameters)
        return self
