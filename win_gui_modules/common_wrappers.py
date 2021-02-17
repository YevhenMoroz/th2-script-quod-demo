from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest, BaseTileData


class BaseTileDetails:
    def __init__(self, base: EmptyRequest = None, window_index: int = None):
        if base is not None and window_index is not None:
            self.base_details = BaseTileData(base=base, windowIndex=window_index)
        elif base is not None:
            self.base_details = BaseTileData(base=base)
        elif window_index is not None:
            self.base_details = BaseTileData(windowIndex=window_index)
        else:
            self.base_details = BaseTileData()

    def set_window_index(self, index: int):
        self.base_details.windowIndex = index

    def set_default_params(self, base_request):
        self.base_details.base.CopyFrom(base_request)

    def build(self):
        return self.base_details
