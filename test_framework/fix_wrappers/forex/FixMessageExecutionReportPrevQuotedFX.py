from datetime import datetime
from custom.tenor_settlement_date import spo, wk1_ndf_maturity, wk2_ndf_maturity, wk3_ndf_maturity, tom
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.forex import FixMessageNewOrderMultiLegFX


class FixMessageExecutionReportPrevQuotedFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    # region SINGLE
    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle,
                                         status: Status = Status.Fill, text: str = None):
        if status is Status.Fill:
            self.__set_fill_sell(new_order_single)
        elif status is Status.Reject:
            self.__set_reject_sell(new_order_single, text)
        else:
            raise Exception("Incorrect Status")
        return self

    def set_params_from_new_order_single_ndf(self, new_order_single: FixMessageNewOrderSingle,
                                             status: Status = Status.Fill):
        if status is Status.Fill:
            self.__set_fill_sell_ndf(new_order_single)
        else:
            raise Exception("Incorrect Status")
        return self

    def set_params_from_new_order_single_ccy2(self, new_order_single: FixMessageNewOrderSingle,
                                              status: Status = Status.Fill):
        if status is Status.Fill:
            self.__set_fill_sell_ccy2(new_order_single)
        else:
            raise Exception("Incorrect Status")
        return self

    # SELL SIDE

    def __set_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            SettlType=new_order_single.get_parameter("SettlType"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=spo(),
            Price="*",
            Account="*",
            OrderCapacity="A",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastMkt="*",
            LastPx="*",
            OrderID="*",
            SettlDate="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            QtyType=0,
            Instrument=new_order_single.get_parameter("Instrument"),
            NoParty="*",
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
        if new_order_single.get_parameter("SettlType") != "0":
            super().add_tag({"LastForwardPoints": "*"})
        return self

    def __set_reject_sell(self, new_order_single: FixMessageNewOrderSingle = None, text: str = None):
        temp = dict(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty="0",
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst="1",
            LastQty="0",
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
            # OrdRejReason="99",
            OrderID="*",
            OrderCapacity="A",
            SettlDate="*",
            ExecType="8",
            LeavesQty="0",
            Text=text if text is not None else "*",
            QtyType="0",
            Instrument=new_order_single.get_parameter("Instrument"),
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

    def __set_fill_sell_ndf(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            SettlType=new_order_single.get_parameter("SettlType"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=tom(),
            Price="*",
            Account="*",
            OrderCapacity="A",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastMkt="*",
            LastPx="*",
            OrderID="*",
            SettlDate="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            QtyType=0,
            Instrument=new_order_single.get_parameter("Instrument"),
            NoParty="*"
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=new_order_single.get_parameter("Instrument")["SecurityType"],
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
            SecurityIDSource="8",
            MaturityDate="*",
            SecurityExchange="*"
        )
        super().update_fields_in_component("Instrument", instrument)
        if new_order_single.get_parameter("SettlType") != "0":
            super().add_tag({"LastForwardPoints": "*"})
        return self

    def __set_fill_sell_ccy2(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][:-4],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            SettlType=new_order_single.get_parameter("SettlType"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=spo(),
            Price="*",
            Account="*",
            OrderCapacity="A",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastMkt="*",
            LastPx="*",
            OrderID="*",
            SettlDate="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            QtyType=0,
            Instrument=new_order_single.get_parameter("Instrument"),
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
        if new_order_single.get_parameter("SettlType") != "0":
            super().add_tag({"LastForwardPoints": "*"})
        return self

    # endregion
    # region SWAP
    def set_params_from_new_order_swap(self, new_order_single: FixMessageNewOrderMultiLegFX,
                                       status: Status = Status.Fill):
        if status is Status.Fill:
            self.__set_fill_sell_swap(new_order_single)
        elif status is Status.Reject:
            self.__set_reject_sell_swap(new_order_single)
        else:
            raise Exception("Incorrect Status")
        return self

    def set_params_from_new_order_swap_ccy2(self, new_order_single: FixMessageNewOrderMultiLegFX):
        self.prepare_swap_ccy2_exec_report(new_order_single)
        if new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "0":
            self.get_parameter("NoLegs")[0].pop("LegLastForwardPoints")
        elif new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "0":
            self.get_parameter("NoLegs")[1].pop("LegLastForwardPoints")
        return self

    def set_params_from_new_order_swap_ndf(self, new_order_single: FixMessageNewOrderMultiLegFX):
        self.prepare_swap_ndf_exec_report(new_order_single)
        return self

    def __set_fill_sell_swap(self, new_order_single: FixMessageNewOrderSingle = None):
        self.prepare_swap_exec_report(new_order_single)
        if new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "0":
            self.get_parameter("NoLegs")[0].pop("LegLastForwardPoints")
        elif new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "0":
            self.get_parameter("NoLegs")[1].pop("LegLastForwardPoints")
        return self

    def __set_reject_sell_swap(self, new_order_single: FixMessageNewOrderSingle = None):
        self.prepare_swap_reject_exec_report(new_order_single)
        return self

    def prepare_swap_exec_report(self, new_order_single: FixMessageNewOrderSingle = None):
        no_legs = [
            dict(LegSide="2" if new_order_single.get_parameter("Side") == "1" else "1",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[0]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[0]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=(new_order_single.get_parameter("Instrument")["Symbol"],
                                new_order_single.get_parameter("Instrument")["Symbol"] + "-SPO-QUODFX") if
                     new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"] == "FXSPOT" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"],
                     LegCurrency=new_order_single.get_parameter("Currency"),
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 ),
            dict(LegSide="1" if new_order_single.get_parameter("Side") == "1" else "2",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[1]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[1]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=(new_order_single.get_parameter("Instrument")["Symbol"],
                                new_order_single.get_parameter("Instrument")["Symbol"] + "-SPO-QUODFX") if
                     new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"] == "FXSPOT" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"],
                     LegCurrency=new_order_single.get_parameter("Currency"),
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 )
        ]
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=spo(),
            Account="*",
            Price="*",
            LastMkt="*",
            LastSwapPoints="*",
            OrderCapacity="A",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            QtyType=0,
            SettlType="*",
            NoParty="*",
            NoLegs=no_legs,
            Instrument=new_order_single.get_parameter("Instrument")
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

    def prepare_swap_ccy2_exec_report(self, new_order_single: FixMessageNewOrderSingle = None):
        no_legs = [
            dict(LegSide="2" if new_order_single.get_parameter("Side") == "1" else "1",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[0]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[0]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=(new_order_single.get_parameter("Instrument")["Symbol"],
                                new_order_single.get_parameter("Instrument")["Symbol"] + "-SPO-QUODFX") if
                     new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"] == "FXSPOT" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"],
                     LegCurrency=new_order_single.get_parameter("Currency"),
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 ),
            dict(LegSide="1" if new_order_single.get_parameter("Side") == "1" else "2",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[1]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[1]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=(new_order_single.get_parameter("Instrument")["Symbol"],
                                new_order_single.get_parameter("Instrument")["Symbol"] + "-SPO-QUODFX") if
                     new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"] == "FXSPOT" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"],
                     LegCurrency=new_order_single.get_parameter("Currency"),
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 )
        ]
        temp = dict(
            Account="*",
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][:-4],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=spo(),
            SettlType="0",
            Price="*",
            LastMkt="*",
            LastSwapPoints="*",
            OrderCapacity="A",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            QtyType=0,
            NoParty="*",
            NoLegs=no_legs,
            Instrument=new_order_single.get_parameter("Instrument")
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

    def prepare_swap_ndf_exec_report(self, new_order_single: FixMessageNewOrderSingle = None):
        no_legs = [
            dict(LegSide="1" if new_order_single.get_parameter("Side") == "2" else "2",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[0]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[0]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=(new_order_single.get_parameter("Instrument")["Symbol"],
                                new_order_single.get_parameter("Instrument")["Symbol"] + "-SPO-QUODFX") if
                     new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"] == "FXSPOT" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"],
                     LegCurrency=new_order_single.get_parameter("Currency"),
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 ),
            dict(LegSide="2" if new_order_single.get_parameter("Side") == "2" else "1",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[1]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[1]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[1]["LegOrderQty"],
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=(new_order_single.get_parameter("Instrument")["Symbol"],
                                new_order_single.get_parameter("Instrument")["Symbol"] + "-SPO-QUODFX") if
                     new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"] == "FXSPOT" else
                     new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[1]["InstrumentLeg"]["LegSecurityType"],
                     LegCurrency=new_order_single.get_parameter("Currency"),
                     LegSecurityExchange="XQFX",
                     LegSecurityIDSource="8",
                 )
                 )
        ]

        if new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "W1":
            no_legs[0]["InstrumentLeg"]["LegMaturityDate"] = wk1_ndf_maturity()
        elif new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "W2":
            no_legs[0]["InstrumentLeg"]["LegMaturityDate"] = wk2_ndf_maturity()
        elif new_order_single.get_parameter("NoLegs")[0]["LegSettlType"] == "W3":
            no_legs[0]["InstrumentLeg"]["LegMaturityDate"] = wk3_ndf_maturity()
        if new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "W1":
            no_legs[1]["InstrumentLeg"]["LegMaturityDate"] = wk1_ndf_maturity()
        elif new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "W2":
            no_legs[1]["InstrumentLeg"]["LegMaturityDate"] = wk2_ndf_maturity()
        elif new_order_single.get_parameter("NoLegs")[1]["LegSettlType"] == "W3":
            no_legs[1]["InstrumentLeg"]["LegMaturityDate"] = wk3_ndf_maturity()

        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=new_order_single.get_parameter("NoLegs")[0]["LegSettlDate"],
            Price="*",
            LastMkt="*",
            LastSwapPoints="*",
            OrderCapacity="A",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            QtyType=0,
            NoParty="*",
            NoLegs=no_legs,
            Instrument=new_order_single.get_parameter("Instrument")
        )
        if new_order_single.get_parameter("Instrument")["Symbol"][-3:] != new_order_single.get_parameter(
                "Currency"):
            temp["SettlCurrency"] = new_order_single.get_parameter("Instrument")["Symbol"][-3:]
        else:
            temp["SettlCurrency"] = new_order_single.get_parameter("Instrument")["Symbol"][:3]
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

    def prepare_swap_reject_exec_report(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty="0",
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            LastQty="0",
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            Price="*",
            LastMkt="*",
            OrderCapacity="A",
            OrdStatus="8",
            TransactTime="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            ExecType="8",
            ExecRestatementReason="*",
            Text="*",
            LeavesQty=0,
            QtyType=0,
            SettlType="*",
            NoParty="*",
            Instrument=new_order_single.get_parameter("Instrument")
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

    # region DepositAndLoan
    def set_params_from_deposit_and_loan(self, new_order_single: FixMessageNewOrderSingle,
                                         status: Status = Status.Fill):
        if status is Status.Fill:
            self.__set_fill_deposit(new_order_single)
        else:
            raise Exception("Incorrect Status")
        return self

    def __set_fill_deposit(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Side=new_order_single.get_parameter("Side"),
            SecondaryClOrdID=new_order_single.get_parameter("SecondaryClOrdID"),
            OrdStatus="2",
            TransactTime="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            LastMkt="XQFX",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="2",
            LeavesQty=0,
            Instrument=new_order_single.get_parameter("Instrument"),
            NoPartyIDs="*"
        )
        super().change_parameters(temp)
        instrument = dict(
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            Product="9"
        )
        super().update_fields_in_component("Instrument", instrument)
        return self

    # endregion

    # region Synergy
    def set_params_from_new_order_single_synergy(self, new_order_single: FixMessageNewOrderSingle,

                                                 status: Status = Status.Fill, text: str = None):
        if status is Status.Fill:
            self.__set_fill_sell_synergy(new_order_single)
        elif status is Status.Reject:
            self.__set_reject_sell_synergy(new_order_single, text)
        else:
            raise Exception("Incorrect Status")
        return self

    def __set_fill_sell_synergy(self, new_order_single: FixMessageNewOrderSingle = None,
                                data_set: BaseDataSet = FxDataSet()):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            VenueType=new_order_single.get_parameter("VenueType"),
            Price=new_order_single.get_parameter("Price"),
            OrdStatus="2",
            SettlCurrAmt="*",
            TransactTime="*",
            LastSpotRate="*",
            AvgPx="*",
            ExecID="*",
            LastMkt="*",
            LastPx="*",
            OrderID="*",
            SettlDate="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="2",
            LeavesQty=0,
            Instrument=new_order_single.get_parameter("Instrument"),
            NoPartyIDs="*",
        )
        super().change_parameters(temp)
        instrument = dict(
            SecurityType=data_set.get_security_type_by_name("fx_spot"),
            Symbol=new_order_single.get_parameter("Instrument")["Symbol"],
            Product="4",
        )
        super().update_fields_in_component("Instrument", instrument)
        # if new_order_single.get_parameter("SettlType") != "0":
        #     super().add_tag({"LastForwardPoints": "*"})
        return self

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

    # endregion
