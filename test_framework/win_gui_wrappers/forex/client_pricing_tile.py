from stubs import Stubs
from test_framework.win_gui_wrappers.base_tile import BaseTile
from win_gui_modules.utils import call


class ClientPricingTile(BaseTile):
    def __init__(self, case_id, session_id, index: int = 0):
        super().__init__(case_id, session_id, index)
        self.cp_service = Stubs.win_act_cp_service
        self.create_tile_call = None
        self.close_tile_call = None

    # region Actions
    def crete_tile(self):
        call(self.create_tile_call, self.base_details.build())
        return self

    def close_tile(self):
        call(self.close_tile_call, self.base_details.build())
    # endregion
