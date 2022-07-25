from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest


class FixMessageOrderCancelRequestAlgo(FixMessageOrderCancelRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_cancel_RFQ(self, nos_rfq: FixMessageNewOrderSingle):
        temp = {
            "ClOrdID": "*",
            "Side": nos_rfq.get_parameter("Side"),
            "TransactTime": "*",
            "Instrument": "*",
            "OrigClOrdID": "*",
            "ExDestination": nos_rfq.get_parameter("ExDestination"),
        }
        super().change_parameters(temp)
        return self
