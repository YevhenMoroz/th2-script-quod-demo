from datetime import datetime
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle


class FixMessageNewOrderSingleTakerDC(FixMessageNewOrderSingle):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(data_set=data_set)
        super().change_parameters(parameters)

    def set_default_sor_from_trade(self, trade_request) -> FixMessageNewOrderSingle:
        request = trade_request.get_parameters()["TradeEntryRequestBlock"]

        base_parameters = {
            "ClOrdID": "*",
            "Account": "*",
            "NoParty": "*",
            "HandlInst": "2",
            "Side": "1" if request["Side"] == "B" else "2",
            "OrderQty": request["ExecQty"],
            "TimeInForce": "0",
            "OrdType": "1",
            "Currency": request["Currency"],
            "SettlCurrency": "*",
            "Instrument": "*",
            "StrategyName": "*",
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
            "SettlType": self.get_data_set().get_settle_type_by_name("spot"),
            "Misc0": trade_request.get_exec_misc_0()

        }
        super().change_parameters(base_parameters)
        return self

    def set_default_mo_from_trade(self, trade_request) -> FixMessageNewOrderSingle:
        request = trade_request.get_parameters()["TradeEntryRequestBlock"]
        base_parameters = {
            "ClOrdID": "*",
            "Account": "*",
            "NoParty": "*",
            "Price": "*",
            "HandlInst": "1",
            "Side": "1" if request["Side"] == "B" else "2",
            "OrderQty": request["ExecQty"],
            "TimeInForce": "4",
            "OrdType": "2",
            "Currency": request["Currency"],
            "SettlCurrency": "*",
            "Instrument": "*",
            "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
            "SettlType": self.get_data_set().get_settle_type_by_name("spot"),
            "Misc0": trade_request.get_exec_misc_0()

        }
        super().change_parameters(base_parameters)
        return self
