from datetime import datetime
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.DataSet import Instrument, Side, Status


class FixMessageExecutionReportAlgo(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None, new_order_single: FixMessageNewOrderSingle = None ):
        super().__init__()
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def set_default_TWAP(self) -> None:
        base_parameters = {
            "Account": "CLIENT1",
            "HandlInst": "0",
            "Side": "1",
            "OrderQty": "1000",
            "TimeInForce": "0",
            "OrdType": "2",
            "TransactTime": datetime.utcnow().isoformat(),
            "OrderCapacity": "A",
            "Price": "20",
            "Currency": "EUR",
            "ExDestination": "XPAR",
            "Instrument": Instrument.FR0010436584,
            "ExecType": "0",
            "OrdStatus": "0",
        }
        super().change_parameters(base_parameters)

    def update_fix_message(self, parameters: dict) -> None:
        super().update_fix_message(parameters)
        temp = dict()
        temp["QuodFlatParameters"] = parameters["QuodFlatParameters"]
        temp["TargetStrategy"] = parameters["TargetStrategy"]
        super().change_parameters(temp)

    def execution_report (self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            Instrument=new_order_single.get_parameter("Instrument"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Price=new_order_single.get_parameter("Price"),
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

    def execution_report_new (self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            Instrument=new_order_single.get_parameter("Instrument"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Price=new_order_single.get_parameter("Price"),
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

    def execution_report_buy (self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Text='*',
            Price=new_order_single.get_parameter("Price"),
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

    def execution_report_fill (self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
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
            Price=new_order_single.get_parameter('Price'),
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

    def execution_report_fill_buy (self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx=new_order_single.get_parameter('Price'),
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
            Price=new_order_single.get_parameter('Price'),
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=0,
            Instrument=new_order_single.get_parameter('Instrument'),
            ExecType='F',
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def execution_report_cancel(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
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
            Price=new_order_single.get_parameter('Price'),
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=0,
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=1005,
            Instrument=new_order_single.get_parameter('Instrument'),
            QtyType='*',
            NoParty='*',
            NoStrategyParameters='*',
            SecAltIDGrp='*',
        )
        super().change_parameters(temp)
        return self

    def execution_report_cancel_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
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

    def change_from_pending_new_to_new(self) -> FixMessageExecutionReport:
        super().change_from_pending_new_to_new()
        self.remove_parameter('Account')
        self.remove_parameter('ExecRestatementReason')
        return self

    def change_buy_from_pending_new_to_new(self) -> FixMessageExecutionReport:
        super().change_from_pending_new_to_new()
        self.change_parameters(dict(OrdStatus= 0, ExecType= 0))
        return self

    def change_buy_from_fill_to_partial_fill(self) -> FixMessageExecutionReport:
        super().change_from_pending_new_to_new()
        self.change_parameter('OrdStatus', '1')
        return self

    def set_params_from_new_order_single(self, side: Side, status: Status):
        if side == Side.Buy.value:
            if Status == Status.Pending.value:
                pass
            elif Status == Status.New.value:
                pass
            elif Status == Status.Fill.value:
                pass
            elif Status == Status.PartialFill.value:
                pass
            elif Status == Status.Cancel.value:
                pass
            else:
                raise Exception(f'Incorrect Status')
        elif side == Side.Sell.value:
            if Status == Status.Pending.value:
                pass
            elif Status == Status.New.value:
                pass
            elif Status == Status.Fill.value:
                pass
            elif Status == Status.PartialFill.value:
                pass
            elif Status == Status.Cancel.value:
                pass
            else:
                raise Exception(f'Incorrect Status')
        else:
            raise Exception(f'Incorrect Side')
