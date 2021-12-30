from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.fix_wrappers.DataSet import GatewaySide, Status
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.forex import FixMessageNewOrderMultiLegFX


class FixMessageExecutionReportPrevQuotedFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    # region SINGLE
    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle, side: GatewaySide,
                                         status: Status, is_forward: bool = False):
        if side is GatewaySide.Buy:
            if status is Status.Pending:
                self.__set_pending_new_buy(new_order_single)
            elif status is Status.New:
                self.__set_new_buy(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_buy(new_order_single)
            else:
                raise Exception('Incorrect Status')
        elif side is GatewaySide.Sell:
            if status is Status.Pending:
                self.__set_pending_new_sell(new_order_single)
            elif status is Status.New:
                self.__set_new_sell(new_order_single)
            elif status is Status.Fill:
                if is_forward:
                    self.__set_fill_sell_fwd(new_order_single)
                else:
                    self.__set_fill_sell(new_order_single)

            else:
                raise Exception('Incorrect Status')
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
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            Instrument=new_order_single.get_parameter("Instrument"),
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
            SpotSettlDate=spo(),
            Price="*",
            OrderCapacity="A",
            OrdStatus='2',
            TradeReportingIndicator='*',
            TransactTime='*',
            LastSpotRate='*',
            AvgPx='*',
            ExecID='*',
            LastPx='*',
            OrderID='*',
            SettlDate='*',
            TradeDate=datetime.today().strftime('%Y%m%d'),
            ExecType='F',
            LeavesQty=0,
            GrossTradeAmt='*',
            ExDestination='*',
            QtyType=0,
            Instrument=new_order_single.get_parameter('Instrument'),
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

    def __set_fill_sell_fwd(self, new_order_single: FixMessageNewOrderSingle = None):
        self.__set_fill_sell(new_order_single)
        self.add_tag({"LastForwardPoints": "*"})
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

    # endregion
    # region SWAP
    def set_params_from_new_order_swap(self, new_order_single: FixMessageNewOrderMultiLegFX, side: GatewaySide,
                                       status: Status):
        if side is GatewaySide.Buy:
            if status is Status.Pending:
                self.__set_pending_new_buy(new_order_single)
            elif status is Status.New:
                self.__set_new_buy(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_buy(new_order_single)
            else:
                raise Exception('Incorrect Status')
        elif side is GatewaySide.Sell:
            if status is Status.Pending:
                self.__set_pending_new_sell(new_order_single)
            elif status is Status.New:
                self.__set_new_sell(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_sell_swap(new_order_single)

            else:
                raise Exception('Incorrect Status')
        return self

    def __set_fill_sell_swap(self, new_order_single: FixMessageNewOrderSingle = None):
        self.prepare_swap_exec_report(new_order_single)
        if new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "0":
            self.get_parameter("NoLegs")[0].pop("LegLastForwardPoints")
        elif new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "0":
            self.get_parameter("NoLegs")[1].pop("LegLastForwardPoints")
        return self

    def prepare_swap_exec_report(self, new_order_single: FixMessageNewOrderSingle = None):
        no_legs = [
            dict(LegSide=new_order_single.get_parameter("NoLegs")[0]["LegSide"],
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[0]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[0]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("OrderQty"),
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=new_order_single.get_parameter("Instrument")["Symbol"] +
                               "-SPO-QUODFX" if new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "0" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"],
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 ),
            dict(LegSide=new_order_single.get_parameter("NoLegs")[1]["LegSide"],
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[1]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[1]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("OrderQty"),
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=new_order_single.get_parameter("Instrument")["Symbol"] +
                               "-SPO-QUODFX" if new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "0" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"],
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 )
        ]
        temp = dict(
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastQty=new_order_single.get_parameter('OrderQty'),
            OrderQty=new_order_single.get_parameter('OrderQty'),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            SpotSettlDate=spo(),
            Price="*",
            LastSwapPoints="*",
            OrderCapacity="A",
            OrdStatus='2',
            TradeReportingIndicator='*',
            TransactTime='*',
            LastSpotRate='*',
            AvgPx='*',
            ExecID='*',
            LastPx='*',
            OrderID='*',
            TradeDate=datetime.today().strftime('%Y%m%d'),
            ExecType='F',
            LeavesQty=0,
            GrossTradeAmt='*',
            ExDestination='*',
            QtyType=0,
            SettlType="*",
            NoParty="*",
            NoLegs=no_legs,
            Instrument=new_order_single.get_parameter('Instrument')
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

    # endregion

    def add_party_role(self):
        party = dict(
            PartyRole="*",
            PartyID="*",
            PartyRoleQualifier="*",
            PartyIDSource="*",
        )
        party_1 = dict(
            PartyRole="*",
            PartyID="*",
            PartyIDSource="*",
        )
        super().add_fields_into_repeating_group("NoParty", [party, party_1, party_1, party_1])
        return self

    def add_party_role_fdw(self):
        party = dict(
            PartyRole="*",
            PartyID="*",
            PartyRoleQualifier="*",
            PartyIDSource="*",
        )
        party_1 = dict(
            PartyRole="*",
            PartyID="*",
            PartyIDSource="*",
        )
        super().update_repeating_group("NoParty", [party, party_1, party_1])
        return self
