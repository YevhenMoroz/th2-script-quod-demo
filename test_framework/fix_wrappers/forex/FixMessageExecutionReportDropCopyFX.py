from datetime import datetime

from custom.tenor_settlement_date import spo
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import GatewaySide, Status
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageExecutionReportDropCopyFX(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(data_set=data_set)
        super().change_parameters(parameters)

    def set_params_from_trade_sor(self, trade_request, response=None):
        request = trade_request.get_parameters()["TradeEntryRequestBlock"]
        temp = dict(
            ClOrdID="*",
            Account="*",
            CumQty=trade_request.get_exec_qty(),
            Currency=request["Currency"],
            HandlInst="2",
            LastQty="*",
            OrderQty=trade_request.get_exec_qty(),
            SettlCurrency="*",
            OrdType="1",
            Side="1" if request["Side"] == "B" else "2",
            SettlType=self.get_data_set().get_settle_type_by_name("spot"),
            TimeInForce="*",
            SpotSettlDate=self.get_data_set().get_settle_date_by_name("spot"),
            StrategyName="1555",
            TargetStrategy="1008",
            OrdStatus="2",
            LastExecutionPolicy="*",
            TradeReportingIndicator="*",
            TransactTime="*",
            LastSpotRate="*",
            SecondaryOrderID="*",
            AvgPx="*",
            ExecID="*",
            LastMkt="*",
            LastPx="*",
            OrderID="*",
            ReplyReceivedTime="*",
            SettlDate="*",
            TradeDate=datetime.today().strftime("%Y%m%d"),
            ExecType="F",
            LeavesQty=0,
            GrossTradeAmt="*",
            ExDestination="*",
            GatingRuleCondName="*",
            GatingRuleName="*",
            QtyType=0,
            Instrument="*",
            SecondaryExecID="*",
            NoParty="*"
        )
        super().change_parameters(temp)

        if response is not None and "Account" in response.get_parameters():
            self.add_tag({"Account": "*"})
        return self

    def set_params_from_trade_mo(self, trade_request, response=None):
        request = trade_request.get_parameters()["TradeEntryRequestBlock"]
        temp = dict(
            ClOrdID="*",
            Account="*",
            CumQty=trade_request.get_exec_qty(),
            Currency=request["Currency"],
            HandlInst="1",
            LastQty="*",
            OrderQty=trade_request.get_exec_qty(),
            SettlCurrency="*",
            OrdType="1",
            Side="*",
            SettlType=self.get_data_set().get_settle_type_by_name("spot"),
            TimeInForce="*",
            SpotSettlDate=self.get_data_set().get_settle_date_by_name("spot"),
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
            Instrument="*",
            NoParty="*"
        )
        super().change_parameters(temp)

        if response is not None and "Account" in response.get_parameters():
            self.add_tag({"Account": "*"})
        return self

    def set_params_from_trade_new(self, trade_request, response=None):
        request = trade_request.get_parameters()["TradeEntryRequestBlock"]
        temp = dict(
            ClOrdID="*",
            Account="*",
            CumQty="0",
            Currency=request["Currency"],
            HandlInst="2",
            LastQty="0",
            OrderQty=trade_request.get_exec_qty(),
            SettlCurrency="*",
            OrdType="1",
            Side="1" if request["Side"] == "B" else "2",
            SettlType=self.get_data_set().get_settle_type_by_name("spot"),
            TimeInForce="*",
            TargetStrategy="1008",
            OrdStatus="0",
            TransactTime="*",
            ExecRestatementReason="*",
            AvgPx="*",
            ExecID="*",
            LastPx="*",
            OrderID="*",
            SettlDate="*",
            ExecType="0",
            LeavesQty=trade_request.get_exec_qty(),
            QtyType=0,
            Instrument="*",
            NoParty="*"
        )
        super().change_parameters(temp)

        if response is not None and "Account" in response.get_parameters():
            self.add_tag({"Account": "*"})
        return self
