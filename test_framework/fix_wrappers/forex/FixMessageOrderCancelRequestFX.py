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
