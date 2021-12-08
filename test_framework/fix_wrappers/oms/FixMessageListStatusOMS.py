from test_framework.fix_wrappers.FixMessageListStatus import FixMessageListStatus
from test_framework.fix_wrappers.FixMessageNewOrderList import FixMessageNewOrderList


class FixMessageListStatusOMS(FixMessageListStatus):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        'NoRpts': '0',
        'ListID': '*',
        'RptSeq': '*',
        'ListStatusType': '1',
        'TotNoOrders': '0',
        'ListOrderStatus': '3',
        'OrdListStatGrp': {'NoOrders': [{
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': '*',
            'LeavesQty': '100',
        }, {
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': '*',
            'LeavesQty': '100',
        }
        ]}
    }

    def set_default_list_status(self, new_order_list: FixMessageNewOrderList):
        no_order = []
        order = {}
        for i in range(len(new_order_list.get_parameter("ListOrdGrp")["NoOrders"])):
            order.update({"AvgPx": "*"})
            order.update({"CumQty": "*"})
            order.update({"ClOrdID": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][i]["ClOrdID"]})
            order.update(
                {"LeavesQty": new_order_list.get_parameter("ListOrdGrp")["NoOrders"][i]["OrderQtyData"]["OrderQty"]})
            no_order.append(order.copy())
        self.change_parameters(self.base_parameters)
        self.change_parameters({'OrdListStatGrp': {'NoOrders': no_order}})
        return self
