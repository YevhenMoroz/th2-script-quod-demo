from inspect import signature

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.win_gui_wrappers.data_set import Side
from win_gui_modules.common_wrappers import BaseTileDetails


class BaseTile:
    def __init__(self, case_id, base_request, index: int = 0):
        self.case_id = case_id
        self.base_request = base_request
        self.extraction_id = bca.client_orderid(4)
        self.base_details = BaseTileDetails(base=self.base_request, window_index=index)
        self.sell_side = Side.sell.value
        self.buy_side = Side.buy.value
        self.verifier = Verifier(self.case_id)

    def clear_details(self, details_list: list):
        for detail in details_list:
            if str(signature(detail.__init__)).find("details") != -1:
                detail.__init__(self.base_details)
            else:
                detail.__init__()