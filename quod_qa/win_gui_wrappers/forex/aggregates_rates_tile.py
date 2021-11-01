from quod_qa.win_gui_wrappers.base_tile import BaseTile
from stubs import Stubs
from win_gui_modules.utils import call


class AggregatesRatesTile(BaseTile):
    def __init__(self, case_id, base_request, index: int = 0):
        super().__init__(case_id, base_request, index)
        self.ar_service = Stubs.win_act_aggregated_rates_service
        self.close_tile_call = None

    # region Actions
    def crete_tile(self):
        call(self.ar_service.createRFQTile, self.base_details.build())
        return self

    def close_tile(self):
        call(self.ar_service.closeRFQTile, self.base_details.build())
    # endregion
