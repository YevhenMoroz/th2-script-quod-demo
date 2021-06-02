from th2_grpc_act_gui_quod import fx_dealing_positions_pb2
from dataclasses import dataclass


@dataclass
class ExtractionPositionsFieldsDetails:
    value: str
    column_name: str


class GetOrdersDetailsRequest:
    def __init__(self):
        self.base_params = None
        self.extraction_id = None
        self.dealing_positions = fx_dealing_positions_pb2.FxDealingPositionsDetailsInfo()

    @staticmethod
    def create(order_info_list: list = None, info=None):
        dealing_positions = GetOrdersDetailsRequest()

        if order_info_list is not None:
            for i in order_info_list:
                dealing_positions.add_positions_info(i)

        if info is not None:
            dealing_positions.add_single_positions_info(info)

        return dealing_positions

    def set_extraction_id(self, extraction_id: str):
        self.extraction_id = extraction_id

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self.dealing_positions.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def add_positions_info(self, positions_info_list: list):
        for positions_info in positions_info_list:
            self.dealing_positions.positionInfo.append(positions_info.build())

    def add_single_positions_info(self, positions_info):
        self.dealing_positions.positionInfo.append(positions_info.build())

    def set_default_params(self, base_request):
        self.base_params = base_request

    def extract_length(self, position_id: str):
        self.dealing_positions.extractPositions = True
        self.dealing_positions.positionId = position_id

    def request(self):
        request = fx_dealing_positions_pb2.GetFxDealingPositionsDetailsRequest()
        request.base.CopyFrom(self.base_params)
        request.extractionId = self.extraction_id
        request.dealingPositionsDetails.CopyFrom(self.dealing_positions)
        return request

    def details(self):
        return self.dealing_positions


class ExtractionPositionsAction:
    def __init__(self):
        self.extraction_action = fx_dealing_positions_pb2.ExtractionPositionsAction()

    @staticmethod
    def create_extraction_action(extraction_detail: ExtractionPositionsFieldsDetails = None, extraction_details: list = None):
        action = ExtractionPositionsAction()
        if extraction_detail is not None:
            action.add_detail(extraction_detail)

        if extraction_details is not None:
            action.add_details(extraction_details)

        return action

    def add_detail(self, detail: ExtractionPositionsFieldsDetails):
        var = self.extraction_action.positionDetails.add()
        var.value = detail.value
        var.colName = detail.column_name

    def add_details(self, details: list):
        for detail in details:
            self.add_detail(detail)

    def build(self):
        return self.extraction_action


class PositionsInfo:
    def __init__(self):
        self.positions_info = fx_dealing_positions_pb2.PositionsInfo()

    @staticmethod
    def create(action=None, actions: list = None, positions_by_currency: GetOrdersDetailsRequest = None):
        positions_info = PositionsInfo()
        if action is not None:
            positions_info.add_single_positions_info(action)

        if actions is not None:
            positions_info.add_positions_info(actions)

        if positions_by_currency is not None:
            positions_info.set_positions_by_currency_details(positions_by_currency)

        return positions_info

    def set_positions_by_currency_details(self, positions_by_currency: GetOrdersDetailsRequest):
        self.positions_info.positionsByCurrency.CopyFrom(positions_by_currency.details())

    def set_number(self, number: int):
        self.positions_info.number = number

    def add_positions_info(self, positions_info_list: list):
        for positions_info in positions_info_list:
            self.add_single_positions_info(positions_info)

    def add_single_positions_info(self, positions_info):
        dealing_positions = fx_dealing_positions_pb2.FxDealingPositionsAction()
        if isinstance(positions_info, ExtractionPositionsAction):
            dealing_positions.extractionAction.CopyFrom(positions_info.build())
        else:
            raise Exception("Unsupported action type")
        self.positions_info.orderActions.append(dealing_positions)

    def build(self):
        return self.positions_info


class FilterPositionsDetails:
    def __init__(self):
        self.base_params = None
        self.filter = None
        self.filter_details = fx_dealing_positions_pb2.FilterDetails()

    @staticmethod
    def create():
        filter_details = FilterPositionsDetails()
        return filter_details.filter_details

    def set_default_params(self, base_request):
        self.base_params = base_request

    def request(self):
        request = fx_dealing_positions_pb2.FilterPositionsDetails()
        request.base.CopyFrom(self.base_params)
        request.filterDetails.CopyFrom(self.filter_details)
        return request

    def set_account(self, account1: str):
        self.filter_details.client = account1

    def set_currency_mode(self, show: bool):
        self.filter_details.showAutoFilterRaw = show

    def expand_positions_by_symbol(self, expand: bool):
        self.filter_details.expandPositionsBySymbol = expand
