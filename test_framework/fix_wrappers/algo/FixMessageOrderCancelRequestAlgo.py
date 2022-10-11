from datetime import datetime

from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest


class FixMessageOrderCancelRequestAlgo(FixMessageOrderCancelRequest):
    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_cancel_RFQ(self, nos_rfq: FixMessageNewOrderSingle):
        temp = {
            "ClOrdID": "*",
            "Side": nos_rfq.get_parameter("Side"),
            "TransactTime": "*",
            "Instrument": "*",
            "OrigClOrdID": "*",
            "ExDestination": nos_rfq.get_parameter("ExDestination"),
        }
        super().change_parameters(temp)
        return self

    def add_header(self):
        if self.is_parameter_exist('header'):
            self.update_fields_in_component('header', {
                'BeginString': '*',
                'SenderCompID': '*',
                'SendingTime': '*',
                'TargetCompID': '*',
                'MsgType': '*',
                'MsgSeqNum': '*',
                'BodyLength': '*',
            })
        else:
            self.add_tag({'header':
                {
                    'BeginString': '*',
                    'SenderCompID': '*',
                    'SendingTime': '*',
                    'TargetCompID': '*',
                    'MsgType': '*',
                    'MsgSeqNum': '*',
                    'BodyLength': '*',
                }
            })
        return self

    def add_DeliverToCompID(self, DeliverToCompID: str):
        self.update_fields_in_component('header', {'DeliverToCompID': DeliverToCompID })
        return self

    def set_cancel_params_for_child(self, nos_child: FixMessageNewOrderSingle):
        temp = dict()
        if nos_child.is_parameter_exist('ShortCode'):
            temp.update(
                ShortCode=nos_child.get_parameter('ShortCode'),
                IClOrdIdAO=nos_child.get_parameter('IClOrdIdAO')
            )
        temp.update(
            Account=nos_child.get_parameter('Account'),
            OrderQty=nos_child.get_parameter('OrderQty'),
            ClOrdID='*',
            OrderID='*',
            TransactTime='*',
            ChildOrderID='*',
            Side=nos_child.get_parameter('Side'),
            Instrument=nos_child.get_parameter('Instrument'),
            ExDestination=nos_child.get_parameter('ExDestination'),
            OrigClOrdID='*'
        )
        super().change_parameters(temp)
        return self
