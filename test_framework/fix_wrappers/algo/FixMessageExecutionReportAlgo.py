from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.DataSet import GatewaySide, Status


class FixMessageExecutionReportAlgo(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle, side: GatewaySide, status: Status):
        if side is GatewaySide.Buy:
            if status is Status.Pending:
                self.__set_pending_new_buy(new_order_single)
            elif status is Status.New:
                self.__set_new_buy(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_buy(new_order_single)
            elif status is Status.PartialFill:
                self.__set_partial_fill_buy(new_order_single)
            elif status is Status.CancelRequest:
                self.__set_cancel_replace_buy(new_order_single)
            elif status is Status.Cancel:
                self.__set_cancel_buy(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        elif side is GatewaySide.Sell:
            if status is Status.Pending:
                self.__set_pending_new_sell(new_order_single)
            elif status is Status.New:
                self.__set_new_sell(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_sell(new_order_single)
            elif status is Status.PartialFill:
                self.__set_partial_fill_sell(new_order_single)
            elif status is Status.Reject:
                self.__set_reject_buy(new_order_single)
            elif status is Status.Cancel:
                self.__set_cancel_sell(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        return self

    def __set_pending_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            Instrument=new_order_single.get_parameter("Instrument"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            TargetStrategy=new_order_single.get_parameter("TargetStrategy"),
            ExecType="A",
            OrdStatus="A",
            TransactTime='*',
            AvgPx='0',
            CumQty='0',
            ExecID='*',
            LastPx='0',
            LastQty='0',
            OrderCapacity='A',
            QtyType='0',
            OrderID='*',
            SettlDate='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            NoParty='*',
            NoStrategyParameters='*',
            SecAltIDGrp='*'
        )
        super().change_parameters(temp)
        return self

    def __set_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            Instrument=new_order_single.get_parameter("Instrument"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            TargetStrategy=new_order_single.get_parameter("TargetStrategy"),
            ExecType="0",
            OrdStatus="0",
            TransactTime='*',
            AvgPx='0',
            CumQty='0',
            ExecID='*',
            LastPx='0',
            LastQty='0',
            OrderCapacity='A',
            QtyType='0',
            OrderID='*',
            SettlDate='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            ExecRestatementReason=4,
            NoParty='*',
            NoStrategyParameters='*',
            SecAltIDGrp='*'
        )
        super().change_parameters(temp)
        return self

    def __set_pending_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Text='*',
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            ExecType="A",
            OrdStatus="A",
            CumQty='0',
            ExecID='*',
            OrderID='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            TransactTime='*',
            AvgPx='*',
            ExDestination='XPAR'
        )
        super().change_parameters(temp)
        return self

    def __set_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Text='*',
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            ExecType="0",
            OrdStatus="0",
            CumQty='0',
            ExecID='*',
            OrderID='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            TransactTime='*',
            AvgPx='*',
            ExDestination='XPAR'
        )
        super().change_parameters(temp)
        return self

    def __set_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastMkt=new_order_single.get_parameter('ExDestination'),
            LastPx='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=2,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            Text='Fill',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty=0,
            SecondaryOrderID='*',
            GrossTradeAmt='*',
            NoParty='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            SecAltIDGrp='*',
            QtyType=0,
            SecondaryClOrdID='*',
            Instrument=new_order_single.get_parameter('Instrument'),
            SecondaryExecID='*'
        )
        super().change_parameters(temp)
        return self

    def __set_partial_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastMkt=new_order_single.get_parameter('ExDestination'),
            LastPx='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=1,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            Text='Partial fill',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty=0,
            SecondaryOrderID='*',
            GrossTradeAmt='*',
            NoParty='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            SecAltIDGrp='*',
            QtyType=0,
            SecondaryClOrdID='*',
            Instrument=new_order_single.get_parameter('Instrument'),
            SecondaryExecID='*'
        )
        super().change_parameters(temp)
        return self

    def __set_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"),
                        LastPx=new_order_single.get_parameter('Price'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx=20,
            ExecID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            ClOrdID='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            Text='Fill',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            OrderID='*',
            TransactTime='*',
            Side=new_order_single.get_parameter('Side'),
            AvgPx='*',
            OrdStatus=2,
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            Instrument=new_order_single.get_parameter('Instrument'),
            ExecType='F',
            ExDestination=new_order_single.get_parameter('ExDestination'),
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_partial_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"),
                        LastPx=new_order_single.get_parameter('Price'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx=20,
            ExecID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            ClOrdID='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            Text='Partial fill',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            OrderID='*',
            TransactTime='*',
            Side=new_order_single.get_parameter('Side'),
            AvgPx='*',
            OrdStatus=1,
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=0,
            Instrument=new_order_single.get_parameter('Instrument'),
            ExecType='F',
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_reject_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx=0,
            ClOrdID='*',
            CumQty=0,
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=8,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=0,
            TransactTime='*',
            SettlDate='*',
            Text= '*',
            ExecType=8,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            Instrument=new_order_single.get_parameter('Instrument'),
            QtyType='*',
            NoParty='*',
            NoStrategyParameters='*',
            SecAltIDGrp='*',
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_replace_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            AvgPx='*',
            ClOrdID='*',
            CumQty='0',
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            OrdStatus=4,
            TimeInForce=3,
            OrigClOrdID='*',
            Side=new_order_single.get_parameter('Side'),
            Text='order canceled',
            TransactTime='*',
            ExecType=4,
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx=0,
            ClOrdID='*',
            CumQty=0,
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            OrdType=new_order_single.get_parameter('OrdType'),
            OrigClOrdID=new_order_single.get_parameter('ClOrdID'),
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=0,
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            Instrument=new_order_single.get_parameter('Instrument'),
            QtyType='*',
            NoParty='*',
            NoStrategyParameters='*',
            SecAltIDGrp='*',
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == 2:
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            AvgPx='*',
            ClOrdID='*',
            CumQty='0',
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            OrigClOrdID='*',
            Side=new_order_single.get_parameter('Side'),
            Text='order canceled',
            TransactTime='*',
            ExecType=4,
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

