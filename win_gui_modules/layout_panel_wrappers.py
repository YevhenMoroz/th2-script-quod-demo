from dataclasses import dataclass, field

from dataclasses import dataclass

from th2_grpc_act_gui_quod import layout_panel_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest


class WorkspaceModificationRequest:
    def __init__(self):
        self.ws_modify_request = layout_panel_pb2.WorkspaceModificationRequest()

    def set_default_params(self, base_request):
        self.ws_modify_request.base.CopyFrom(base_request)

    def set_path(self, path: str):
        self.ws_modify_request.Sides = path

    def set_filename(self, filename: str):
        self.ws_modify_request.fileName = filename

    def do_import(self):
        self.ws_modify_request.actionType = layout_panel_pb2.WorkspaceModificationRequest.ActionType.IMPORT

    def do_export(self):
        self.ws_modify_request.actionType = layout_panel_pb2.WorkspaceModificationRequest.ActionType.EXPORT

    def build(self):
        return self.ws_modify_request


@dataclass
class CustomCurrencySlippage:
    instrument: str= ''
    dmaSlippage: str= ''
    algoSlippage: str= ''
    removeRowNumber: str = 0

@dataclass
class DefaultFXValues:
    custom_currency_slippage_list : list
    AggressiveOrderType: str = ''
    AggressiveTIF: str = ''
    AggressiveStrategyType: str = ''
    AggressiveStrategy: str = ''
    AggressiveChildStrategy: str = ''
    PassiveOrderType: str = ''
    PassiveTIF: str = ''
    PassiveStrategyType: str = ''
    PassiveStrategy: str = ''
    PassiveChildStrategy: str = ''
    AlgoSlippage: str = ''
    DMASlippage: str = ''
    Client: str = ''

class OptionOrderTicketRequest:
    def __init__(self, base: EmptyRequest = None):
        self.request = layout_panel_pb2.OptionOrderTicketRequest(base=base)

    def set_default_fx_values(self, values: DefaultFXValues):
        fx_panel = layout_panel_pb2.OptionOrderTicketRequest.DefaultFXValues()
        fx_panel.AggressiveOrderType.value = values.AggressiveOrderType
        fx_panel.AggressiveTIF.value = values.AggressiveTIF
        fx_panel.AggressiveStrategyType.value = values.AggressiveStrategyType
        fx_panel.AggressiveStrategy.value = values.AggressiveStrategy
        fx_panel.AggressiveChildStrategy.value = values.AggressiveChildStrategy
        fx_panel.PassiveOrderType.value = values.PassiveOrderType
        fx_panel.PassiveTIF.value = values.PassiveTIF
        fx_panel.PassiveStrategyType.value = values.PassiveStrategyType
        fx_panel.PassiveStrategy.value = values.PassiveStrategy
        fx_panel.PassiveChildStrategy.value = values.PassiveChildStrategy
        fx_panel.AlgoSlippage.value = values.AlgoSlippage
        fx_panel.DMASlippage.value = values.DMASlippage
        fx_panel.Client.value = values.Client

        for customSlipage in values.custom_currency_slippage_list:
            cp = fx_panel.customCurrencySlippage.add()
            cp.instrument = customSlipage.instrument
            cp.dmaSlippage = customSlipage.dmaSlippage
            cp.algoSlippage = customSlipage.algoSlippage
            cp.removeRowNumber = customSlipage.removeRowNumber

        self.request.defaultFXValues.CopyFrom(fx_panel)


    def build(self):
        return self.request


class FXConfigsRequest:
    def __init__(self, base: EmptyRequest):
        self.request = layout_panel_pb2.FXConfigsRequest(base=base)

    def set_cumulative_qty(self, value: str):
        self.request.CumulativeQtyChartPips.value = value

    def set_one_click_mode(self, value: str):
        self.request.OneClickOrdersMode.value = value

    def set_algo_default_qty(self, value: str):
        self.request.AlgoDefaultQty.value = value

    def set_headers_prices_format(self, value: str):
        self.request.HeaderPricesFormat.value = value

    def build(self):
        return self.request
