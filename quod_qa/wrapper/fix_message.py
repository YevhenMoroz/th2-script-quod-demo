from custom import basic_custom_actions as bca


class FixMessage:

    def __init__(self, parameters=''):
        self.parameters = parameters

    def get_parameters(self):
        return self.parameters

    def change_parameter(self, parametr_name, new_parametr_value):
        self.parameters[parametr_name] = new_parametr_value

    def change_parameters(self, parameter_list):
        for key in parameter_list:
            self.parameters[key] = parameter_list[key]

    def get_parameter(self, parametr_name):
        return self.parameters[parametr_name]

    def add_tag(self, parameter):
        self.parameters.update(parameter)

    def remove_tag(self, parameter_name):
        self.parameters.pop(parameter_name)

    def get_ClOrdID(self):
        return self.parameters['ClOrdID']

    def add_random_ClOrdID(self):
        self.parameters.update({'ClOrdID': bca.client_orderid(9)})

