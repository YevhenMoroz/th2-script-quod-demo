from custom import basic_custom_actions
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from datetime import datetime


class FixMessageOrderCancelReplaceRequestAlgo(FixMessageOrderCancelReplaceRequest):
    def __init__(self, new_order_single: FixMessageNewOrderSingle = None, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)
        self.__update_fix_message(new_order_single)

    # set_DMA_params
    def set_DMA_params(self) -> FixMessageOrderCancelReplaceRequest:
        base_parameters = {
            "Account": "XPAR_CLIENT2",
            'ClOrdID': '*',
            'Currency': 'EUR',
            'HandlInst': '1',
            'OrderQty': '1000',
            'OrdType': '2',
            'Price': '20',
            'Side': '1',
            'Instrument': '*',
            'TimeInForce': '0',
            "TransactTime": '*',
            'SettlDate': '*',
            'ExDestination': "XPAR",
            'OrderCapacity': 'A',
            'NoParty': '*',
            # 'Origin': '*'
        }
        super().change_parameters(base_parameters)
        return self

    def __update_fix_message(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.is_parameter_exist('Price'):
            temp.update(Price=new_order_single.get_parameter('Price'))
        if new_order_single.is_parameter_exist('StopPx'):
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if new_order_single.is_parameter_exist('DisplayInstruction'):
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(
                ClientAlgoPolicyID=new_order_single.get_parameter('ClientAlgoPolicyID'),
            )
        if new_order_single.is_parameter_exist('IClOrdIdAO'):
            temp.update(IClOrdIdAO='OD_5fgfDXg-00',)
        if new_order_single.is_parameter_exist('ShortCode'):
            temp.update(ShortCode='17536')
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('NoStrategyParameters') and new_order_single.get_parameter('TargetStrategy') != '1004':
            temp.update(NoStrategyParameters=new_order_single.get_parameter('NoStrategyParameters'))
        if new_order_single.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy=new_order_single.get_parameter('TargetStrategy'))
        if new_order_single.is_parameter_exist('ExDestination'):
            temp.update(ExDestination=new_order_single.get_parameter('ExDestination'))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('PegInstructions'):
            temp.update(PegInstructions=new_order_single.get_parameter('PegInstructions'))
        if new_order_single.is_parameter_exist('TriggeringInstruction'):
            temp.update(TriggeringInstruction=new_order_single.get_parameter('TriggeringInstruction'))
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
            Currency=new_order_single.get_parameter('Currency'),
            Instrument=new_order_single.get_parameter('Instrument'),
            OrigClOrdID=new_order_single.get_parameter("ClOrdID"),
        )
        if new_order_single.get_parameter('ClOrdID') == '*':                                            # for checking modification request on child
            temp.update(
                OrderID='*',
                TransactTime='*',
            )
        super().change_parameters(temp)
        return self