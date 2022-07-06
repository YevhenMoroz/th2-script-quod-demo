from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from datetime import datetime


class FixMessageOrderCancelReplaceRequestAlgo(FixMessageOrderCancelReplaceRequest):
    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)
        self.__update_fix_message(new_order_single)

    def __update_fix_message(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(
                ClientAlgoPolicyID=new_order_single.get_parameter('ClientAlgoPolicyID'),
                IClOrdIdAO='OD_5fgfDXg-00',
                ShortCode='17536'
            )
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('NoStrategyParameters') and new_order_single.get_parameter('TargetStrategy') != '1004':
            temp.update(NoStrategyParameters=new_order_single.get_parameter('NoStrategyParameters'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            HandlInst=new_order_single.get_parameter('HandlInst'),
            Side=new_order_single.get_parameter('Side'),
            OrderQty=new_order_single.get_parameter('OrderQty'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            OrdType=new_order_single.get_parameter('OrdType'),
            TransactTime=datetime.utcnow().isoformat(),
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            Price=new_order_single.get_parameter('Price'),
            Currency=new_order_single.get_parameter('Currency'),
            Instrument=new_order_single.get_parameter('Instrument'),
            OrigClOrdID=new_order_single.get_parameter("ClOrdID"),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
        )
        super().change_parameters(temp)
        return self
