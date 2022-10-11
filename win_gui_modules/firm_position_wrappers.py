import enum
from enum import Enum
from typing import List
from th2_grpc_act_gui_quod import risk_management_pb2


@enum.unique
class FieldForExtraction(Enum):
    DAILY_PL = 'DAILY_PL'
    MONTH_PL = 'MONTH_PL'
    YEAR_PL = 'YEAR_PL'
    WEEK_PL = 'WEEK_PL'
    QUARTER_PL = 'QUARTER_PL'
    UNREALIZED_PL = 'UNREALIZED_PL'


class ExtractPositionsDetails:
    def __init__(self, base_request=None):
        if base_request:
            self.__position_details = risk_management_pb2.ExtractPositionsDetails()
            self.__position_details.base.CopyFrom(base_request)
        else:
            self.__position_details = risk_management_pb2.ExtractPositionsDetails()

    def set_default_param(self, base_request):
        self.__position_details.CopyFrom(base_request)

    def set_security_account(self, security_account):
        self.__position_details.securityAccount = security_account

    def set_filter(self, filter_dict: dict):
        self.__position_details.filter.update(filter_dict)

    def set_extraction_of_columns(self, columns: list):
        for column in columns:
            self.__position_details.columnNames.append(column)

    def set_field_from_panel(self, panel_fields: list):
        for field in panel_fields:
            if 'DAILY_PL' in FieldForExtraction.__members__:
                self.__position_details.panelFields.append(eval(f'risk_management_pb2.{field}'))
            else:
                raise ValueError('Error message')

    def build(self):
        return self.__position_details
