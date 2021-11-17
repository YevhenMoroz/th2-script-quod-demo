from quod_qa.wrapper_test.FixMessageListStatus import FixMessageListStatus


class FixMessageListStatusOMS(FixMessageListStatus):

    def set_default_list(self):
        base_parameters = {
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
        super().change_parameters(base_parameters)
