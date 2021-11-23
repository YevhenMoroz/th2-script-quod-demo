from datetime import datetime

from quod_qa.wrapper_test.FixMessageNewOrderList import FixMessage, FixMessageNewOrderList


class FixMessageListStatus(FixMessage):

    def __init__(self, new_order_list: FixMessageNewOrderList = None, parameters: dict = None):
        super().__init__(message_type="ListStatus")
        if new_order_list is not None:
            self.update_fix_message(new_order_list.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict) -> FixMessage:
        temp = dict(
            NoRpts="*",
            ListID=parameters["ListID"],
            RptSeq="*",
            ListStatusType="*",
            ListOrderStatus=parameters["ListOrderStatus"],
            OrdListStatGrp=parameters["OrdListStatGrp"],
        )
        super().change_parameters(temp)
        return self
