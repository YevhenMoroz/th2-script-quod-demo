from datetime import datetime

from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
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

    def set_params_for_order(self, order: FixMessageNewOrderSingle):
        base_parameters = {
            "OrigClOrdID": order.get_parameter("ClOrdID"),
            "ClOrdID": order.get_parameter("ClOrdID"),
            "Account": order.get_parameter("Account"),
            "Side": order.get_parameter("Side"),
            "TransactTime": datetime.utcnow().isoformat(),
        }
        super().change_parameters(base_parameters)
        return self
