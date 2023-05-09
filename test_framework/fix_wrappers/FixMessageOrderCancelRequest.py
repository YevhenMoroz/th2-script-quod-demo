from datetime import datetime

from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle


class FixMessageOrderCancelRequest(FixMessage):

    def __init__(self, new_order_single: FixMessageNewOrderSingle or FixMessage = None, parameters: dict = None):
        super().__init__(message_type="OrderCancelRequest")
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> None:
        temp = dict(
            OrigClOrdID=parameters["ClOrdID"],
            ClOrdID=parameters["ClOrdID"],
            Account=parameters["Account"],
            Side=parameters["Side"],
            TransactTime=datetime.utcnow().isoformat(),
        )
        super().change_parameters(temp)