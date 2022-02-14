from datetime import datetime

from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageOrderCancelRejectReportOMS(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__(message_type="OrderCancelRejectRequest")
        if new_order_single is not None:
            self.change_parameters(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message_cancel_replace_request(self, parameters: dict) -> None:
        temp = dict(
            OrderID=parameters["ClOrdID"],
            ClOrdID=parameters["ClOrdID"],
            OrigClOrdID=parameters["ClOrdID"],
            OrderStatus='0',
            CxlRejResponseTo='2'
        )
        super().change_parameters(temp)

    def update_fix_message_cancel_request(self, parameters: dict) -> None:
        temp = dict(
            OrderID=parameters["ClOrdID"],
            ClOrdID=parameters["ClOrdID"],
            OrigClOrdID=parameters["ClOrdID"],
            OrderStatus='0',
            CxlRejResponseTo='1'
        )
        super().change_parameters(temp)