from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from datetime import datetime


class FixMessageOrderCancelReplaceRequestAlgo(FixMessageOrderCancelReplaceRequest):

    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__()
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_fix_message(self, parameters: dict):
        temp = dict(
            Account=parameters['Account'],
            ClOrdID=parameters['ClOrdID'],
            HandlInst=parameters['HandlInst'],
            Side=parameters['Side'],
            OrderQty=parameters['OrderQty'],
            TimeInForce=parameters['TimeInForce'],
            OrdType=parameters['OrdType'],
            TransactTime=datetime.utcnow().isoformat(),
            OrderCapacity=parameters['OrderCapacity'],
            Price=parameters['Price'],
            Currency=parameters['Currency'],
            Instrument=parameters['Instrument'],
            OrigClOrdID=parameters["ClOrdID"],
            TargetStrategy=parameters['TargetStrategy'],
            NoStrategyParameters=parameters['NoStrategyParameters']
        )
        super().change_parameters(temp)
        return self
