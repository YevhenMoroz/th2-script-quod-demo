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

    # def set_no_orders(self, num: int, cl_ord_id=None, leaves_qty=None, avg_px=None, cum_qty=None):
    #     self.change_parameters(self.base_parameters)
    #     if cl_ord_id is not None:
    #         self.base_parameters['OrdListStatGrp']['NoOrders'][num]['ClOrdID'] = cl_ord_id
    #     if leaves_qty is not None:
    #         self.base_parameters['OrdListStatGrp']['NoOrders'][num]['LeavesQty'] = leaves_qty
    #     if avg_px is not None:
    #         self.base_parameters['OrdListStatGrp']['NoOrders'][num]['AvgPx'] = avg_px
    #     if cum_qty is not None:
    #         self.base_parameters['OrdListStatGrp']['NoOrders'][num]['CumQty'] = cum_qty
    #     return self

    def set_default_list_status(self, new_order_list: FixMessageNewOrderList):
        change_parameters = dict()
        for ord in new_order_list.get_parameter("ListOrdGrp")["NoOrders"]:
            self.base_parameters['OrdListStatGrp']['NoOrders'][num]['ClOrdID'] = cl_ord_id
        return self

