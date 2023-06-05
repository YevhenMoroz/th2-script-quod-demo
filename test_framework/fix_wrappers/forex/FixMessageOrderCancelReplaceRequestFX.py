from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest


class FixMessageOrderCancelReplaceRequestFX(FixMessageOrderCancelReplaceRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_set_default_params(self, order_id):
        base_parameters = {
            "ClOrdID": "*",
            "OrderID": order_id,
            "OrigClOrdID": order_id,
            "OrderQty": "*",
            "OrdType": "1",
            "TimeInForce": "*",

        }
        super().change_parameters(base_parameters)
        return self
