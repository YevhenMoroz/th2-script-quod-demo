from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from test_framework.fix_wrappers.FixMessageOrderCancelRejectReport import FixMessageOrderCancelRejectReport
from test_framework.data_sets.constants import GatewaySide, Status


class FixMessageOrderCancelRejectReportAlgo(FixMessageOrderCancelRejectReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle, side: GatewaySide, status: Status):
        if side is GatewaySide.Buy:
            if status is Status.Reject:
                self.__set_reject_buy(new_order_single)
            elif status is Status.New:
                self.__set_new_buy(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        elif side is GatewaySide.Sell:
            if status is Status.New:
                self.__set_new_sell(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        elif side is GatewaySide.KeplerSell:
            if status is Status.New:
                self.__set_new_kepler_sell(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        return self

    def __set_reject_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            OrderID='*',
            ClOrdID='*',
            OrigClOrdID='*',
            OrdStatus='8',
            CxlRejResponseTo='1',
            Text='cancel reject',
            TransactTime='*'
        )
        super().change_parameters(temp)
        return self

    def __set_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            OrderID='*',
            ClOrdID='*',
            OrigClOrdID='*',
            OrdStatus='0',
            CxlRejResponseTo='2',
            Text='Modify rejection',
            TransactTime='*'
        )
        super().change_parameters(temp)
        return self

    def __set_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011'] or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(
                SecondaryAlgoPolicyID='*',
            )
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            OrderID='*',
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            OrigClOrdID='*',
            OrdStatus='0',
            CxlRejResponseTo='1',
            Text='*',
            TransactTime='*',
        )
        super().change_parameters(temp)
        return self

    def __set_new_kepler_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011', '1008']:
            temp.update(
                SecondaryAlgoPolicyID='*',
            )
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            OrderID='*',
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            OrigClOrdID='*',
            OrdStatus='0',
            CxlRejResponseTo='1',
            Text='*',
            TransactTime='*',
        )
        super().change_parameters(temp)
        return self
