from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.data_sets.constants import Status
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle,
                                         status: Status = Status.Fill,
                                         response=None):

        if status is Status.Fill:
            self.__set_fill_sell(new_order_single, response)
        elif status is Status.Reject:
            self.__set_reject_sell(new_order_single, response)
        elif status is Status.PartialFill:
            self.__set_partialfill_sell(new_order_single, response)
        else:
            raise Exception(f"Incorrect Status")
        return self

    def __set_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None, response=None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty=new_order_single.get_parameter("OrderQty"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst="1",
            LastQty=new_order_single.get_parameter("OrderQty"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            SettlType=new_order_single.get_parameter("SettlType"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=spo(),
            Price="*",
            OrdStatus="2",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            LastMkt="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            OrderCapacity="A",
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
        if new_order_single.get_parameter('SettlType') != "0":
            super().add_tag({"LastForwardPoints": "*"})
        if response is not None:
            if "Account" in response.get_parameters():
                self.add_tag({"Account": "*"})
        return self

    def __set_partialfill_sell(self, new_order_single: FixMessageNewOrderSingle = None, response=None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            CumQty="*",
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst="1",
            LastQty="*",
            OrderQty=new_order_single.get_parameter("OrderQty"),
            SettlCurrency=new_order_single.get_parameter("Instrument")["Symbol"][-3:],
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            SettlType=new_order_single.get_parameter("SettlType"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            SpotSettlDate=spo(),
            Price="*",
            OrdStatus="4",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            LastMkt="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            OrderCapacity="A",
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
        if new_order_single.get_parameter('SettlType') != "0":
            super().add_tag({"LastForwardPoints": "*"})
        if response is not None:
            if "Account" in response.get_parameters():
                self.add_tag({"Account": "*"})
        return self

    def __set_reject_sell(self, new_order_single: FixMessageNewOrderSingle = None, response=None):
        temp = dict(
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
            OrderID="*",
            OrderCapacity="A",
            SettlDate="*",
            ExecType="8",
            LeavesQty="0",
            Text="*",
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
        if response is not None:
            if "Account" in response.get_parameters():
                self.add_tag({"Account": "*"})
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
