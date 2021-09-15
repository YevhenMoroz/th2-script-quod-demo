from th2_grpc_act_gui_quod import basket_ticket_pb2
from th2_grpc_act_gui_quod.basket_ticket_pb2 import FileDetails
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


class BasketTicketDetails:
    def __init__(self):
        self._request = basket_ticket_pb2.BasketTicketDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_name_value(self, name: str):
        self._request.name = name

    def set_basket_template_name(self, name: str):
        self._request.basketTemplateName = name

    def set_client_value(self, client: str):
        self._request.client = client

    def set_date_value(self, date: str):
        self._request.date = date

    def set_time_in_force_value(self, time_in_force: str):
        self._request.timeInForce = time_in_force

    def set_file_details(self, file_details: FileDetails):
        self._request.fileDetails.CopyFrom(file_details)

    def set_row_details(self, row_details: list):
        for details in row_details:
            self._request.rowsDetails.append(details)

    def build(self):
        return self._request


class FileDetails:
    def __init__(self, file_type=None, path_to_file: str = None):
        self._request = basket_ticket_pb2.FileDetails()
        self._request.fileType = file_type
        self._request.pathToFile = path_to_file

    def set_file_type(self, file_type):
        self._request.fileType = file_type

    def set_path_to_file(self, path_to_file: str):
        self._request.pathToFile = path_to_file

    def build(self):
        return self._request


class RowDetails:
    def __init__(self, filtration_value: str = None, delete_row: bool = None, values: dict = None):
        self._request = basket_ticket_pb2.RowDetails()
        self._request.filtrationValue = filtration_value
        self._request.deleteRow = delete_row
        if values is not None:
            self._request.values.update(values)

    def set_filtration_value(self, filtration_value: str):
        self._request.filtrationValue = filtration_value

    def set_delete_row(self, delete_row: bool):
        self._request.deleteRow = delete_row

    def set_values(self, values: dict):
        self._request.values = values

    def build(self):
        return self._request


class ExtractTemplateDetails:

    def __init__(self, base_request=None, filter: dict = None, column_names: list = None):
        if base_request is not None:
            self._request = basket_ticket_pb2.ExtractTemplateDetails(base=base_request)
        else:
            self._request = basket_ticket_pb2.ExtractTemplateDetails()
        if filter is not None:
            self._request.filter.update(filter)

        if column_names is not None:
            for column in column_names:
                self._request.columnNames.append(column)

    def set_base_details(self, base_details):
        self._request.base.CopyFrom(base_details)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_column_names(self, column_names: list):
        for column in column_names:
            self._request.columnNames.append(column)

    def build(self):
        return self._request


class FileType(Enum):
    EXCEL = basket_ticket_pb2.FileType.EXCEL
    CSV = basket_ticket_pb2.FileType.CSV
