from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import MDAMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class MarketDataSnapshotFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=MDAMessageType.MarketDataSnapshotFullRefresh.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {}
        super().change_parameters(base_parameters)

    def get_timestamps(self):
        orig_venue_id = self.get_parameter("OrigVenueID")
        orig_md_time = self.get_parameter("OrigMDTime")
        orig_md_arrival_time = self.get_parameter("OrigMDArrivalTime")
        return [orig_venue_id, orig_md_time, orig_md_arrival_time]
