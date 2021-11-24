from inspect import signature

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from test_framework.win_gui_wrappers.data_set import Side
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import get_base_request


class BaseTile:
    def __init__(self, case_id, session_id, index: int = 0):
        self.case_id = case_id
        self.base_request = get_base_request(session_id, case_id)
        self.extraction_id = bca.client_orderid(4)
        self.base_details = BaseTileDetails(base=self.base_request, window_index=index)
        self.base_data = BaseTileData(base=self.base_request)
        self.sell_side = Side.sell.value
        self.buy_side = Side.buy.value
        self.verifier = Verifier(self.case_id)

    def clear_details(self, details_list: list):
        for detail in details_list:
            if str(signature(detail.__init__)).find("details") != -1:
                detail.__init__(self.base_details)
            else:
                detail.__init__()

    def compare_values(self, expected_value: str, actual_value: str, event_name: str = "Compare values",
                       ver_method: VerificationMethod = VerificationMethod.EQUALS, value_name: str = "Value"):
        self.verifier.set_event_name(event_name)
        self.verifier.compare_values(value_name, expected_value, actual_value, ver_method)
        self.verifier.verify()
