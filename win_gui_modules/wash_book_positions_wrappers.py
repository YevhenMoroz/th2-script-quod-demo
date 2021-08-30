
from dataclasses import dataclass

from th2_grpc_act_gui_quod import wash_book_positions_pb2
from th2_grpc_act_gui_quod.wash_book_positions_pb2 import WashBookPositionsDetailsInfo, \
    GetWashBookPositionsDetailsRequest, WashBookPositionsInfo, \
    WashBookPositionsAction


@dataclass
class ExtractionWashBookPositionsFieldsDetails:
    value: str
    column_name: str


class GetWashBookDetailsRequest:
    def __init__(self):
        self.base_params = None
        self.extraction_id = None
        self.security_account = None
        self.wash_book_positions = WashBookPositionsDetailsInfo()

    @staticmethod
    def create(order_info_list: list = None, info=None):
        wash_book_positions = GetWashBookDetailsRequest()

        if order_info_list is not None:
            for i in order_info_list:
                wash_book_positions.add_positions_info(i)

        if info is not None:
            wash_book_positions.add_single_positions_info(info)

        return wash_book_positions

    def set_extraction_id(self, extraction_id: str):
        self.extraction_id = extraction_id

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.wash_book_positions.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def add_positions_info(self, positions_info_list: list):
        for positions_info in positions_info_list:
            self.wash_book_positions.positionInfo.append(positions_info.build())

    def add_single_positions_info(self, positions_info):
        self.wash_book_positions.positionInfo.append(positions_info.build())

    def set_default_params(self, base_request):
        self.base_params = base_request

    def set_security_account(self, security_account: str):
        self.security_account = security_account

    def extract_length(self, position_id: str):
        self.wash_book_positions.extractPositions = True
        self.wash_book_positions.positionId = position_id

    def request(self):
        request = GetWashBookPositionsDetailsRequest()
        request.base.CopyFrom(self.base_params)
        request.extractionId = self.extraction_id
        request.securityAccount = self.security_account
        request.washBookPositionsDetails.CopyFrom(self.wash_book_positions)
        return request

    def details(self):
        return self.wash_book_positions


class ExtractionWashBookPositionsAction:
    def __init__(self):
        self.extraction_action = wash_book_positions_pb2.ExtractionWashBookPositionsAction()

    @staticmethod
    def create_extraction_action(extraction_detail: ExtractionWashBookPositionsFieldsDetails = None, extraction_details: list = None):
        action = ExtractionWashBookPositionsAction()
        if extraction_detail is not None:
            action.add_detail(extraction_detail)

        if extraction_details is not None:
            action.add_details(extraction_details)

        return action

    def add_detail(self, detail: ExtractionWashBookPositionsFieldsDetails):
        var = self.extraction_action.positionDetails.add()
        var.value = detail.value
        var.colName = detail.column_name

    def add_details(self, details: list):
        for detail in details:
            self.add_detail(detail)

    def build(self):
        return self.extraction_action


class WashPositionsInfo:
    def __init__(self):
        self.positions_info = WashBookPositionsInfo()

    @staticmethod
    def create(action=None, actions: list = None):
        positions_info = WashPositionsInfo()
        if action is not None:
            positions_info.add_single_positions_info(action)

        if actions is not None:
            positions_info.add_positions_info(actions)

        return positions_info

    def set_number(self, number: int):
        self.positions_info.number = number

    def add_positions_info(self, positions_info_list: list):
        for positions_info in positions_info_list:
            self.add_single_positions_info(positions_info)

    def add_single_positions_info(self, positions_info):
        dealing_positions = WashBookPositionsAction()
        if isinstance(positions_info, ExtractionWashBookPositionsAction):
            dealing_positions.extractionAction.CopyFrom(positions_info.build())
        else:
            raise Exception("Unsupported action type")
        self.positions_info.orderActions.append(dealing_positions)

    def build(self):
        return self.positions_info
