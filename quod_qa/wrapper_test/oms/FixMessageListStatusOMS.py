from quod_qa.wrapper_test.FixMessageListStatus import FixMessageListStatus


class FixMessageListStatusOMS(FixMessageListStatus):
    def __init__(self, parameters: dict = None):
        super().__init__()
        self.change_parameters(parameters)

    base_parameters = {
        'NoRpts':'0',
        'ListID': '*',
        'RptSeq': '*',
        'ListStatusType':'1',
        'TotNoOrders':'0',
        'ListOrderStatus': '3',
        'OrdListStatGrp': {'NoOrders': [{
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': '*',
            'LeavesQty': '900',
        }, {
            'AvgPx': '0',
            'CumQty': '0',
            'ClOrdID': '*',
            'LeavesQty': '900',
        }
        ]}
    }

    def set_default_list_status(self):
        self.change_parameters(self.base_parameters)
        return self
