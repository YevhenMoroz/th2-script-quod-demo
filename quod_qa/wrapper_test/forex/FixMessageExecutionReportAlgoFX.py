from datetime import datetime
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.DataSet import Instrument


class FixMessageExecutionReportAlgoFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None, new_order_single: FixMessageNewOrderSingle = None):
        super().__init__()
        if new_order_single is not None:
            self.update_fix_message(new_order_single.get_parameters())
        super().change_parameters(parameters)

    def update_to_pending_new(self, new_order_single: FixMessageNewOrderSingle) -> None:
        initial = new_order_single.get_parameters()
        temp = dict(
            ExecType="A",
            OrdStatus="A",
            Account=initial["Account"],
            LeavesQty=initial["OrderQty"],
            Currency=initial["Currency"],
            SettlCurrency=initial["Instrument"]["Symbol"][-3:],
            AvgPx="*",
            LastPx="*",
            QtyType="*",
            CumQty="*",
            LastQty="*",
            HandlInst="2",
        )
        super().change_parameters(temp)
        instr = dict(
            SecurityIDSource="8",
            SecurityID=initial["Instrument"]["Symbol"],
            Product="4",
            SecurityExchange="*",
        )
        super().update_fields_in_component("Instrument", instr)
        self.add_party_role()

    def update_to_pending_new_sor(self, new_order_single_sor: FixMessageNewOrderSingle) -> None:
        self.update_to_pending_new(new_order_single_sor)
        initial_sor = new_order_single_sor.get_parameters()
        super().add_tag({"TargetStrategy": "1008"})
        self.add_fields_into_repeating_group("NoStrategyParameters", initial_sor["NoStrategyParameters"])

    def update_to_filled_sor(self, new_order_single_sor: FixMessageNewOrderSingle):
        initial = new_order_single_sor.get_parameters()
        self.update_to_pending_new_sor(new_order_single_sor)
        temp = dict(
            ExecType="F",
            OrdStatus="2",
            CumQty=initial["OrderQty"],
            LastQty=initial["OrderQty"],
            LastSpotRate="*",
            AvgPx="*",
            LastPx="*",
            SecondaryOrderID="*",
            LastMkt="*",
            Text="*",
            SettlType="*",
            SecondaryExecID="*",
            ExDestination="*",
            GrossTradeAmt="*",
            SettlDate="*",
            LastExecutionPolicy="*",
            TradeDate="*",
            TradeReportingIndicator="*",
            LeavesQty="0",
        )
        self.change_parameters(temp)
        return self




    def add_party_role(self):
        party = dict(
            PartyRole="*",
            PartyID="*",
            PartyIDSource="*",
        )
        super().add_fields_into_repeating_group("NoParty", [party])
        return self
