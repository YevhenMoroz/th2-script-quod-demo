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
