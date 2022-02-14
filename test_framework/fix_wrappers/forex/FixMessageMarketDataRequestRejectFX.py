from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.fix_wrappers.FixMessageMarketDataRequestReject import FixMessageMarketDataRequestReject


class FixMessageMarketDataRequestRejectFX(FixMessageMarketDataRequestReject):
    def __init__(self, parameters: dict = None):
        super().__init__(parameters)
        super().change_parameters(parameters)

    def set_md_reject_params(self, md_request, text: str = None):
        md_reject_params = {
            "MDReqID": md_request.get_parameter("MDReqID"),
            "MDReqRejReason": "3",
            "Text": text if text is not None else "*"
        }
        super().change_parameters(md_reject_params)
        return self
