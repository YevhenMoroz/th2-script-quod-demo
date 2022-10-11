from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.data_sets.constants import GatewaySide, Status
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportAlgoFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle,
                                         side: GatewaySide = GatewaySide.Sell,
                                         status: Status = Status.Fill):
        if side is GatewaySide.Buy:
            if status is Status.Pending:
                self.__set_pending_new_buy(new_order_single)
            elif status is Status.New:
                self.__set_new_buy(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_buy(new_order_single)
            elif status is Status.PartialFill:
                self.__set_partial_fill_buy(new_order_single)
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
            elif status is Status.Cancel:
                self.__set_cancel_sell(new_order_single)
            elif status is Status.Reject:
                self.__set_reject_sell(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        return self

    # SELL SIDE
    # CHECKED
    def __set_pending_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Side=new_order_single.get_parameter("Side"),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            OrdType=new_order_single.get_parameter("OrdType"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Account=new_order_single.get_parameter("Account"),
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            Instrument=new_order_single.get_parameter("Instrument"),
            SettlDate=new_order_single.get_parameter("SettlDate"),
            NoStrategyParameters=new_order_single.get_parameter("NoStrategyParameters"),
            ExecID="*",
            OrderID="*",
            ExecType="A",
            OrdStatus="A",
            AvgPx="*",
            Price="*",
            TransactTime="*",
            LastPx="*",
            QtyType="*",
            CumQty="*",
            LastQty="*",
            HandlInst="2",
            TargetStrategy="1008",
            StrategyName="1555",
            NoParty="*"
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityIDSource="8",
            Product="4",
            SecurityExchange="*",
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

    # CHECKED
    def __set_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            Instrument=new_order_single.get_parameter("Instrument"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            SettlType=new_order_single.get_parameter("SettlType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            TargetStrategy=new_order_single.get_parameter("TargetStrategy"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            NoStrategyParameters=new_order_single.get_parameter("NoStrategyParameters"),
            ExecType="0",
            Price="*",
            StrategyName="1555",
            OrdStatus="0",
            TransactTime='*',
            AvgPx='0',
            CumQty='0',
            ExecID='*',
            LastPx='0',
            LastQty='0',
            QtyType='0',
            OrderID='*',
            SettlDate='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            ExecRestatementReason=4,
            NoParty="*"
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            Product="4",
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

    # CHECKED
    def __set_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastQty=new_order_single.get_parameter('OrderQty'),
            OrderQty=new_order_single.get_parameter('OrderQty'),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            SettlType=new_order_single.get_parameter('SettlType'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            NoStrategyParameters="*",
            SpotSettlDate=spo(),
            StrategyName='1555',
            Price="*",
            TargetStrategy='1008',
            OrdStatus='2',
            LastExecutionPolicy='*',
            TradeReportingIndicator='*',
            TransactTime='*',
            LastSpotRate='*',
            SecondaryOrderID='*',
            AvgPx='*',
            ExecID='*',
            LastMkt='*',
            LastPx='*',
            OrderID='*',
            Text='*',
            ReplyReceivedTime='*',
            SettlDate='*',
            TradeDate=datetime.today().strftime('%Y%m%d'),
            ExecType='F',
            LeavesQty=0,
            GrossTradeAmt='*',
            ExDestination='*',
            QtyType=0,
            Instrument=new_order_single.get_parameter('Instrument'),
            SecondaryExecID='*',
            NoParty="*"
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityIDSource="8",
            Product="4",
            SecurityExchange="*",
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

    # TODO: doublecheck
    def __set_partial_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ReplyReceivedTime="*",
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty="*",
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            LastSpotRate='*',
            StrategyName='*',
            SecondaryOrderID='*',
            SpotSettlDate=spo(),
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx='*',
            LastQty='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=1,
            OrdType=new_order_single.get_parameter('OrdType'),
            Price=new_order_single.get_parameter('Price'),
            Side=new_order_single.get_parameter('Side'),
            Text='Hello sim',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            NoStrategyParameters=new_order_single.get_parameter("NoStrategyParameters"),
            TransactTime='*',
            SettlDate='*',
            TradeDate='*',
            ExecType='F',
            LastMkt='*',
            SettlType=new_order_single.get_parameter('SettlType'),
            LeavesQty="*",
            TradeReportingIndicator='0',
            GrossTradeAmt='*',
            NoParty='*',
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            LastExecutionPolicy='*',
            ExDestination='*',
            QtyType=0,
            Instrument=new_order_single.get_parameter('Instrument'),
            SecondaryExecID='*'
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityIDSource="8",
            Product="4",
            SecurityExchange="*",
        )
        super().update_fields_in_component("Instrument", instrument)
        # self.add_party_role()
        return self

    # TODO: doublecheck
    def __set_cancel_sell(self, new_order_single: FixMessageNewOrderSingle = None):
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

    def __set_reject_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            Currency=new_order_single.get_parameter('Currency'),
            CumQty="0",
            ExecID='*',
            ExecType='8',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            Instrument=new_order_single.get_parameter('Instrument'),
            LastPx='*',
            LastQty="0",
            LeavesQty=0,
            NoParty="*",
            OrderCapacity="A",
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus='8',
            OrdType=new_order_single.get_parameter('OrdType'),
            Price="*",
            QtyType=0,
            SettlDate='*',
            Side=new_order_single.get_parameter('Side'),
            StrategyName='1555',
            TargetStrategy='1008',
            Text='*',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*'
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            Product="4",
            SecurityExchange="*",
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

    # BUY SIDE
    # TODO: doublecheck
    def __set_pending_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
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

    # TODO: doublecheck
    def __set_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Text='*',
            Price=new_order_single.get_parameter("Price"),
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

    # TODO: doublecheck
    def __set_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx=new_order_single.get_parameter('Price'),
            ExecID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            ClOrdID='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            Text='*',
            ReplyReceivedTime='*',
            LastSpotRate='*',
            SettlCurrency='*',
            SettlDate=new_order_single.get_parameter('SettlDate'),
            SpotSettlDate=spo(),
            OrderID='*',
            TransactTime='*',
            LastExecutionPolicy='*',
            Side=new_order_single.get_parameter('Side'),
            AvgPx='*',
            NoParty='*',
            QtyType='*',
            SettlType=new_order_single.get_parameter('SettlType'),
            SecondaryOrderID='*',
            OrderCapacity='*',
            OrdStatus=2,
            HandlInst="*",
            TradeReportingIndicator="0",
            TradeDate=datetime.today().strftime('%Y%m%d'),
            Price=new_order_single.get_parameter('Price'),
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            Instrument=new_order_single.get_parameter('Instrument'),
            SecondaryExecID='*',
            ExDestination=new_order_single.get_parameter('ExDestination'),
            GrossTradeAmt="*",
            ExecType='F',
            LeavesQty=0
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityIDSource="8",
            Product="4",
            SecurityExchange=new_order_single.get_parameter('ExDestination'),
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

    # TODO: doublecheck
    def __set_partial_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx=new_order_single.get_parameter('Price'),
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
            Price=new_order_single.get_parameter('Price'),
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=0,
            Instrument=new_order_single.get_parameter('Instrument'),
            ExecType='F',
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    # TODO: doublecheck
    def __set_cancel_buy(self, new_order_single: FixMessageNewOrderSingle = None):
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

    def add_party_role(self):
        party = dict(
            PartyRole="*",
            PartyID="*",
            PartyRoleQualifier="*",
            PartyIDSource="*",
        )
        super().add_fields_into_repeating_group("NoParty", [party])
        return self

    def __set_reject_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty="0",
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst="*",
            LastQty="*",
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            SettlType=new_order_single.get_parameter("SettlType"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            Price="*",
            LastMkt="*",
            OrdStatus="8",
            TransactTime="*",
            ExecRestatementReason="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            OrderCapacity="A",
            SettlDate="*",
            ExecType="8",
            LeavesQty="0",
            Text="*",
            QtyType="0",
            Instrument=new_order_single.get_parameter("Instrument"),
            NoParty="*",
            TargetStrategy="*"
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityIDSource="8",
            Product="4",
            SecurityExchange="*",
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

