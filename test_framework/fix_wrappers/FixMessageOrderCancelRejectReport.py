from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageOrderCancelRejectReport(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__(message_type=FIXMessageType.OrderCancelRejectReport.value)
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> None:
        temp = dict(
            OrderID=parameters["ClOrdID"],
            ClOrdID=parameters["ClOrdID"],
            OrigClOrdID=parameters["ClOrdID"],
            OrderStatus='0',
            CxlRejResponseTo='2'
        )
        super().change_parameters(temp)