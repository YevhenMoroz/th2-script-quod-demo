from th2_grpc_act_gui_quod import basket_ticket_pb2
from utils.enum import Enum


class TemplatesDetails:
    def __init__(self):
        self._request = basket_ticket_pb2.TemplatesDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_name_value(self, name: str):
        self._request.name = name

    def set_exec_policy(self, exec_policy: str):
        self._request.execPolicy = exec_policy

    def set_default_client(self, client: str):
        self._request.defaultClient = client

    def set_description(self, description: str):
        self._request.description = description

    def set_symbol_source(self, symbol_source: str):
        self._request.symbolSource = symbol_source

    def set_time_in_force(self, time_in_force: str):
        self._request.timeInForce = time_in_force

    def set_imported_file_mapping_details(self, details):
        self._request.importedFileMappingDetails.CopyFrom(details)

    def build(self):
        return self._request


class ImportedFileMappingDetails:
    def __init__(self, has_header: bool = None, fields_details: list = None):
        self._request = basket_ticket_pb2.ImportedFileMappingDetails()
        self._request.hasHeader = has_header
        if fields_details is not None:
            for detail in fields_details:
                self._request.fieldDetails.append(detail)

    def set_has_header(self, has_header: bool):
        self._request.hasReader = has_header

    def set_field_details(self, fields_details: list):
        for detail in fields_details:
            self._request.fieldDetails.append(detail)

    def build(self):
        return self._request


class ImportedFileMappingFieldDetails:
    def __init__(self, field=None, column_number_value: str = None,
                 default_value: str = None):
        self._request = basket_ticket_pb2.ImportedFileMappingFieldDetails()
        self._request.field = field
        self._request.columnNumberValue = column_number_value
        self._request.defaultValue = default_value

    def set_field(self, field):
        self._request.field = field

    def set_column_number_value(self, column_number_value: str):
        self._request.columnNumberValue = column_number_value

    def set_default_value(self, default_value: str):
        self._request.defaultValue = default_value

    def build(self):
        return self._request


class ImportedFieldMappingField(Enum):
    SYMBOL = basket_ticket_pb2.ImportedFileMappingField.SYMBOL
    QUANTITY = basket_ticket_pb2.ImportedFileMappingField.QUANTITY
    PRICE = basket_ticket_pb2.ImportedFileMappingField.PRICE
    SIDE = basket_ticket_pb2.ImportedFileMappingField.SIDE
    ORD_TYPE = basket_ticket_pb2.ImportedFileMappingField.ORD_TYPE
    STOP_PRICE = basket_ticket_pb2.ImportedFileMappingField.STOP_PRICE
    ACCOUNT = basket_ticket_pb2.ImportedFileMappingField.ACCOUNT
    CAPACITY = basket_ticket_pb2.ImportedFileMappingField.CAPACITY