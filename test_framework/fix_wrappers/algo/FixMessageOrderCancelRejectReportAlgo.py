from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessage, FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from test_framework.fix_wrappers.FixMessageOrderCancelRejectReport import FixMessageOrderCancelRejectReport
from test_framework.data_sets.constants import GatewaySide, Status


class FixMessageOrderCancelRejectReportAlgo(FixMessageOrderCancelRejectReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    # def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle, side: GatewaySide, status: Status):
    #     if side is GatewaySide.Buy:
    #         if status is Status.Eliminate:
    #             self.__set_eliminate_buy(new_order_single)
    #         else:
    #             raise Exception(f'Incorrect Status')
    #     elif side is GatewaySide.Sell:
    #         if status is Status.New:
    #             self.__set_new_sell(new_order_single)
    #         else:
    #             raise Exception(f'Incorrect Status')
    #     return self
    #
    # def __set_eliminate_buy(self, new_order_single: FixMessageNewOrderSingle = None):
    #     temp = dict()
    #     temp.update(
    #         Account='*',
    #         OrderID='*',
    #         ClOrdID='*',
    #         OrigClOrdID='*',
    #         OrdStatus='0',
    #         CxlRejResponseTo='1',
    #         Text='cancel reject',
    #         TransactTime='*'
    #     )
    #     super().change_parameters(temp)
    #     return self
    #
    # def __set_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
    #     temp = dict()
    #     temp.update(
    #         Account=new_order_single.get_parameter('Account'),
    #         OrderID='*',
    #         ClOrdID=new_order_single.get_parameter("ClOrdID"),
    #         OrigClOrdID='*',
    #         OrdStatus="0",
    #         CxlRejResponseTo='1',
    #         Text='cancel reject',
    #         TransactTime='*',
    #     )
    #     super().change_parameters(temp)
    #     return self

    def update_fix_message(self, parameters: dict) -> None:
        temp = dict(
            Account='*',
            OrderID=parameters["ClOrdID"],
            ClOrdID=parameters["ClOrdID"],
            OrigClOrdID=parameters["ClOrdID"],
            OrdStatus='0',
            CxlRejResponseTo='1',
            Text='cancel reject',
            TransactTime='*'
        )
        super().change_parameters(temp)