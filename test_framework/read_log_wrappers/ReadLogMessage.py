from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet


class ReadLogMessage:

    def __init__(self, message_type: str, data_set: BaseDataSet = None):
        self.__parameters = dict()
        self.__message_type = message_type
        self.__data_set = data_set

    def get_message_type(self) -> str:
        return self.__message_type

    def is_parameter_exist(self, key: str) -> bool:
        return key in self.__parameters

    def get_parameter(self, parameter_name: str):
        return self.__parameters[parameter_name]

    def get_parameters(self) -> dict:
        return self.__parameters

    def change_parameter(self, parameter_name: str, new_parameter_value):
        self.__parameters[parameter_name] = new_parameter_value
        return self

    def change_parameters(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.__parameters[key] = parameter_list[key]
        return self

    def add_parameter(self, parameter: dict):
        self.__parameters.update(parameter)
        return self

    def remove_parameter(self, parameter_name: str):
        self.__parameters.pop(parameter_name)
        return self

    def remove_parameters(self, parameter_name_list: list):
        for par in parameter_name_list:
            self.__parameters.pop(par)
        return self

    def get_data_set(self):
        return self.__data_set

    def delete_group(self, field):
        del self.__parameters[field]
