from datetime import datetime

from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList


class FixMessageListCancelRequest(FixMessage):

    def __init__(self,  new_order_list: FixMessageNewOrderList = None, parameters: dict = None):
        super().__init__(message_type="ListCancelRequest")
        if new_order_list is not None:
            self.update_fix_message(new_order_list.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> None:
        temp = dict(
            ListID=parameters["ListID"],
            TransactTime=datetime.utcnow().isoformat(),
        )
        super().change_parameters(temp)