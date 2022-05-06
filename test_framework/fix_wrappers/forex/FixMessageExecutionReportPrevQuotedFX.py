from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.data_sets.constants import Status
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.forex import FixMessageNewOrderMultiLegFX


class FixMessageExecutionReportPrevQuotedFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    # region SINGLE
    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle, status: Status):
        if status is Status.Fill:
            self.__set_fill_sell(new_order_single)
        else:
            raise Exception('Incorrect Status')
        return self

    # SELL SIDE

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
        if new_order_single.get_parameter('SettlType') != "0":
            super().add_tag({"LastForwardPoints": "*"})
        return self

    # endregion
    # region SWAP
    def set_params_from_new_order_swap(self, new_order_single: FixMessageNewOrderMultiLegFX, status: Status):
        if status is Status.Fill:
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
            dict(LegSide="2" if new_order_single.get_parameter("Side") == "1" else "1",
                 LegOrderQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegSettlDate=new_order_single.get_parameter("NoLegs")[0]["LegSettlDate"],
                 LegSettlType=new_order_single.get_parameter("NoLegs")[0]["LegSettlType"],
                 LegLastQty=new_order_single.get_parameter("NoLegs")[0]["LegOrderQty"],
                 LegLastForwardPoints="*",
                 LegPrice="*",
                 LegLastPx="*",
                 InstrumentLeg=dict(
                     LegSymbol=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityID=new_order_single.get_parameter("Instrument")["Symbol"],
                     LegSecurityType=new_order_single.get_parameter("NoLegs")[0]["InstrumentLeg"]["LegSecurityType"],
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
                     LegSymbol=new_order_single.get_parameter("Instrument")["Symbol"],
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
            LastMkt="*",
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

    # region DepositAndLoan
    def set_params_from_deposit_and_loan(self, new_order_single: FixMessageNewOrderSingle, status: Status):
        if status is Status.Fill:
            self.__set_fill_deposit(new_order_single)
        else:
            raise Exception('Incorrect Status')
        return self

    def __set_fill_deposit(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            OrderQty=new_order_single.get_parameter('OrderQty'),
            Side=new_order_single.get_parameter('Side'),
            SecondaryClOrdID=new_order_single.get_parameter('SecondaryClOrdID'),
            OrdStatus='2',
            TransactTime='*',
            AvgPx='*',
            ExecID='*',
            LastPx='*',
            OrderID='*',
            LastMkt='XQFX',
            TradeDate=datetime.today().strftime('%Y%m%d'),
            ExecType='2',
            LeavesQty=0,
            Instrument=new_order_single.get_parameter('Instrument'),
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
