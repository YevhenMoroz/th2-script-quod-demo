from datetime import datetime

from custom import basic_custom_actions
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageOrderCancelReplaceRequest(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__(message_type="OrderCancelReplaceRequest")
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> None:
        temp = dict(
            OrigClOrdID=basic_custom_actions.client_orderid(9),
            ClOrdID=parameters["ClOrdID"],
            Account=parameters["Account"],
            Side=parameters["Side"],
            TransactTime=datetime.utcnow().isoformat(),
        )
        super().change_parameters(temp)