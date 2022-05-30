class TradingRestApiMessage:
    def __init__(self, request_type_http, response_type_http=None, message_type_web_socket=None, data_set=None):
        self.parameters = dict()
        self.key_fields_http_response = dict()
        self.key_fields_web_socket_response = dict()
        self.request_type_http = request_type_http
        self.response_type_http = response_type_http
        self.message_type_web_socket = message_type_web_socket
        self.data_set = data_set

    def get_parameters(self):
        return self.parameters

    def get_request_type_http(self):
        return self.request_type_http

    def get_response_type_http(self):
        return self.response_type_http

    def get_message_type_web_socket(self):
        return self.message_type_web_socket

    def change_key_fields_http_response(self, key_fields):
        self.key_fields_http_response = key_fields

    def change_key_fields_web_socket_response(self, key_fields):
        self.key_fields_web_socket_response = key_fields

    def change_parameter(self, parameter_name: str, new_parameter_value) -> None:
        self.parameters[parameter_name] = new_parameter_value

    def change_parameter_in_component(self, component_name: str, fields: dict):
        new_component = self.parameters[component_name]
        if isinstance(new_component, list):
            new_component_to_dict = new_component[0]
            new_component_to_dict.update(fields)
        elif isinstance(new_component, dict):
            new_component.update(fields)
        return self

    def change_parameters(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.parameters[key] = parameter_list[key]
        return self

    def change_parameters_for_instrument(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.parameters['Instrument'][key] = parameter_list[key]
        return self

    def remove_parameter(self, parameter_name: str):
        self.parameters.pop(parameter_name)
        return self

    def remove_parameters(self, parameter_name_list: list):
        for par in parameter_name_list:
            self.parameters.pop(par)
        return self


