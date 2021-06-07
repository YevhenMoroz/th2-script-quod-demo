from enum import Enum

from th2_grpc_act_gui_quod import common_pb2
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


class CommissionsDetails:
    def __init__(self, commission_details: common_pb2.CommissionsDetails()):
        self.request = commission_details

    def toggle_manual(self):
        self.request.toggleManual = True

    def add_commission(self, basis: str = None, rate: str = None, amount: str = None, currency: str = None):
        var = self.request.commissionsTableParams.add()
        if basis is not None:
            var.basis = basis
        if rate is not None:
            var.rate = rate
        if amount is not None:
            var.amount = amount
        if currency is not None:
            var.currency = currency

    def remove_commissions(self):
        self.request.removeCommissions = True


class SpreadAction(Enum):
    WIDEN_SPREAD = common_pb2.WIDEN_SPREAD
    NARROW_SPREAD = common_pb2.NARROW_SPREAD
    INCREASE_ASK = common_pb2.INCREASE_ASK
    DECREASE_ASK = common_pb2.DECREASE_ASK
    INCREASE_BID = common_pb2.INCREASE_BID
    DECREASE_BID = common_pb2.DECREASE_BID
    SKEW_TOWARDS_BID = common_pb2.SKEW_TOWARDS_BID
    SKEW_TOWARDS_ASK = common_pb2.SKEW_TOWARDS_ASK


class ContainedRow:
    def __init__(self, message: common_pb2.TableCheckDetails.ContainedRow()):
        self.message = message

    def set_row_id(self, row_id: str):
        self.message.rowId = row_id

    def set_row_number(self, row_number: int):
        self.message.rowNumber = row_number

    def set_params(self, row_params: dict):
        self.message.params.update(row_params)


class TableCheckDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = common_pb2.TableCheckDetails(base=base)
        else:
            self._request = common_pb2.TableCheckDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filters: dict):
        self._request.filter.update(filters)

    def add_contained_rows(self):
        var = self._request.containedRows.add()
        return ContainedRow(message=var)

    def build(self):
        return self._request


class MoveWindowDetails:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = common_pb2.MoveWindowDetails(base=base)
        else:
            self._request = common_pb2.MoveWindowDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_from_x_offset(self, from_x_offset: str):
        self._request.fromXOffset = from_x_offset

    def set_from_y_offset(self, from_y_offset: str):
        self._request.fromYOffset = from_y_offset

    def set_to_x_offset(self, to_x_offset: str):
        self._request.toXOffset = to_x_offset

    def set_to_y_offset(self, to_y_offset: str):
        self._request.toYOffset = to_y_offset

    def set_from_offset(self, from_x_offset: str, from_y_offset: str):
        self._request.fromXOffset = from_x_offset
        self._request.fromYOffset = from_y_offset

    def set_to_offset(self, to_x_offset: str, to_y_offset: str):
        self._request.toXOffset = to_x_offset
        self._request.toYOffset = to_y_offset

    def close_window(self):
        self._request.closeWindow = True

    def build(self):
        return self._request
