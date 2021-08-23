from custom import basic_custom_actions as bca


class FixMessage:

    def __init__(self, message_type: str):
        self.parameters = dict()
        self.message_type = message_type

    def get_parameters(self):
        return self.parameters

    def change_parameter(self, parametr_name, new_parametr_value):
        self.parameters[parametr_name] = new_parametr_value

    def change_parameters(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.parameters[key] = parameter_list[key]

    def get_parameter(self, parametr_name):
        return self.parameters[parametr_name]

    def add_tag(self, parameter):
        self.parameters.update(parameter)

    def remove_tag(self, parameter_name):
        self.parameters.pop(parameter_name)