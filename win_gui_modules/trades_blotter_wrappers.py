from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest

from dataclasses import dataclass

from th2_grpc_act_gui_quod import trades_pb2


class MatchDetails:

    def __init__(self):
        self.match_details = trades_pb2.MatchDetails()

    def set_qty_to_match(self, qty_to_match: str):
        self.match_details.qtyToMatch = qty_to_match

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.match_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def click_match(self):
        self.match_details.matchConfirmAction = trades_pb2.MatchDetails.MatchConfirmAction.MATCH

    def click_cancel(self):
        self.match_details.matchConfirmAction = trades_pb2.MatchDetails.MatchConfirmAction.CANCEL

    def build(self):
        return self.match_details


class ModifyTradesDetails:
    def __init__(self, match_details: MatchDetails):
        self.modify_trades_details = trades_pb2.ModifyTradesDetails()
        self.modify_trades_details.tradesDetails.CopyFrom(match_details.build())

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.modify_trades_details.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_default_params(self, base_request):
        self.modify_trades_details.base.CopyFrom(base_request)

    def set_selected_rows(self, row_numbers: list):
        self.modify_trades_details.selectedRows.extend(row_numbers)

    def set_order_to_match(self, order_to_match: str):
        self.modify_trades_details.orderToMatch = order_to_match

    def build(self):
        return self.modify_trades_details


class CancelManualExecutionDetails:
    def __init__(self):
        self.cancel_manual_execution_details = trades_pb2.CancelManualExecutionDetails()

    def set_filter(self, filter: dict):
        self.cancel_manual_execution_details.tradesWindowFilter.update(filter)

    def set_default_params(self, base_request):
        self.cancel_manual_execution_details.base.CopyFrom(base_request)

    def build(self):
        return self.cancel_manual_execution_details


class ExtractTradesBookSubLvlDataDetails:
    def __init__(self):
        self.details = trades_pb2.ExtractTradesBookSubLvlDataDetails()

    def set_default_params(self, base_request):
        self.details.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self.details.filter.update(filter)

    def set_column_names(self, column_names: list):
        self.details.columnNames.extend(column_names)

    def set_row_number(self, row_number):
        self.details.rowsNumber = row_number

    def set_tab_name(self, tab_name):
        self.details.tabName = tab_name

    def build(self):
        return self.details
