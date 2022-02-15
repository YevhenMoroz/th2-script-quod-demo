from stubs import Stubs
from test_framework.win_gui_wrappers.base_positions_window import BasePositionsBook
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, PositionsInfo
from custom import basic_custom_actions as bca



class FXPositions(BasePositionsBook):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.positions_info = PositionsInfo()
        self.position_details = GetOrdersDetailsRequest()
        self.get_positions_details_call = Stubs.act_fx_dealing_positions.getFxDealingPositionsDetails
        self.extraction_id = bca.client_orderid(4)
        self.position_details = GetOrdersDetailsRequest()
        self.position_details.set_extraction_id(self.extraction_id)
        self.position_details.set_default_params(base_request=self.base_request)









