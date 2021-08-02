from th2_grpc_act_gui_quod import ar_operations_pb2
from th2_grpc_act_gui_quod.ar_operations_pb2 import QuoteRequestDetailsInfo
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest
from th2_grpc_act_gui_quod.order_book_pb2 import ExtractionAction

from win_gui_modules.order_book_wrappers import ExtractionDetail


class QuoteDetailsRequest:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = ar_operations_pb2.QuoteDetailsRequest(base=base)
        else:
            self._request = ar_operations_pb2.QuoteDetailsRequest()

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self._request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self._request.extractionFields.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_details(self, details: list):
        for detail in details:
            self.add_extraction_detail(detail)

    def set_extraction_id(self, extraction_id: str):
        self._request.extractionId = extraction_id

    def set_row_number(self, row_number: int):
        self._request.rowNumber = row_number

    def request(self) -> ar_operations_pb2.QuoteDetailsRequest:
        return self._request






# class QuoteRequestDetailsRequest:
#     def __init__(self):
#         self.base_params = None
#         self.extraction_id = None
#         self.orderDetails = QuoteRequestDetailsInfo()
#
#     @staticmethod
#     def create(order_info_list: list = None, info=None):
#         order_details = QuoteRequestDetailsRequest()
#
#         if order_info_list is not None:
#             for i in order_info_list:
#                 order_details.add_single_order_info(i)
#
#         if info is not None:
#             order_details.add_single_order_info(info)
#
#         return order_details
#
#     def set_extraction_id(self, extraction_id: str):
#         self.extraction_id = extraction_id
#
#     def set_filter(self, filter_list: list):
#         length = len(filter_list)
#         i = 0
#         while i < length:
#             self.orders_details.filter[filter_list[i]] = filter_list[i + 1]
#             i += 2
#
#     def set_order_info(self, order_info_list: list):
#         for order_info in order_info_list:
#             self.orders_details.quoteRequestInfo.append(order_info.build())
#
#     def add_single_order_info(self, order_info):
#         self.orders_details.quoteRequestInfo.append(order_info.build())
#
#     def set_default_params(self, base_request):
#         self.base_params = base_request
#
#     def extract_length(self, count_id: str):
#         self.orders_details.extractCount = True
#         self.orders_details.countId = count_id
#
#     def request(self):
#         request = ar_operations_pb2.QuoteRequestDetailsRequest()
#         request.base.CopyFrom(self.base_params)
#         request.extractionId = self.extraction_id
#         request.orderDetails.CopyFrom(self.orders_details)
#         return request
#
#     def details(self):
#         return self.orders_details
#
# class QuoteRequestInfo:
#     def __init__(self):
#         self.order_info = ar_operations_pb2.QuoteRequestInfo()
#
#     @staticmethod
#     def create(action=None, actions: list = None, sub_order_details: QuoteRequestDetailsRequest = None):
#         order_info = QuoteRequestInfo()
#         if action is not None:
#             order_info.add_single_order_action(action)
#
#         if actions is not None:
#             order_info.add_order_actions(actions)
#
#         if sub_order_details is not None:
#             order_info.set_sub_orders_details(sub_order_details)
#
#         return order_info
#
#     def set_sub_orders_details(self, sub_order_details: QuoteRequestDetailsRequest):
#         self.order_info.subOrders.CopyFrom(sub_order_details.details())
#
#     def set_number(self, number: int):
#         self.order_info.number = number
#
#     def add_order_actions(self, actions: list):
#         for action in actions:
#             self.add_single_order_action(action)
#
#     def add_single_order_action(self, action):
#         order_action = ar_operations_pb2.QuoteRequestAction()
#         # if isinstance(action, OrderAnalysisAction):
#         #     order_analysis = order_book_pb2.OrderAnalysis()
#         #     order_analysis.orderAnalysisAction.append(action.build())
#         #     order_action.orderAnalysis.CopyFrom(order_analysis)
#         # elif isinstance(action, ExtractionAction):
#         order_action.extractionAction.CopyFrom(action.build())
#         # else:
#             # raise Exception("Unsupported action type")
#         self.order_info.orderActions.append(order_action)
#
#     def build(self):
#         return self.order_info
#
# class QuoteRequestAction:
#     def __init__(self):
#         self.row_selector = ar_operations_pb2.QuoteRequestAction()
#
#     def set_column_name(self, extractionFieldsDetails: ExtractionAction):
#         self.row_selector.extractionFieldsDetails = extractionFieldsDetails
#
#     def reject(self):
#         self.row_selector.compareType = ar_operations_pb2.QuoteRequestAction.ContextActionsQuoteBook.REJECT
#
#     def unassign(self):
#         self.row_selector.compareType = ar_operations_pb2.QuoteRequestAction.ContextActionsQuoteBook.UNASSIGN
#
#     def extract(self):
#         self.row_selector.compareType = ar_operations_pb2.QuoteRequestAction.ContextActionsQuoteBook.EXTRACT
#
#     def build(self):
#         return self.row_selector