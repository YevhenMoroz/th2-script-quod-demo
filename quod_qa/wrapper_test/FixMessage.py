from custom import basic_custom_actions

class FixMessage:

    def __init__(self, message_type: str):
        self.__parameters = dict()
        self.__message_type = message_type

    def get_message_type(self) -> str:
        return self.__message_type

    def get_parameter(self, parameter_name: str):
        return self.__parameters[parameter_name]

    def get_parameters(self) -> dict:
        return self.__parameters

    def change_parameter(self, parameter_name: str, new_parameter_value: str) -> None:
        self.__parameters[parameter_name] = new_parameter_value

    def change_parameters(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.__parameters[key] = parameter_list[key]
        return self

    def add_tag(self, parameter: dict) -> None:
        self.__parameters.update(parameter)

    def remove_parameter(self, parameter_name: str) -> None:
        self.__parameters.pop(parameter_name)

    def add_ClordId(self, ClOrdID):
        self.change_parameter("ClOrdID", ClOrdID + " " + basic_custom_actions.client_orderid(9))
        return self

    def print_parameters(self) -> None:
        #TODO
        pass

    def update_fields_in_component(self, component: str, fields: dict):
        new_component = self.get_parameter(component)
        new_component.update(fields)

        self.change_parameters({component: new_component})
        return self

    def remove_fields_from_component(self, component: str, fields: list):
        new_component = self.get_parameter(component)
        for key in fields:
            if key not in new_component:
                raise Exception(f'Unknown argument for removing from component', key)
            else:
                new_component.pop(key)

        self.change_parameters({component: new_component})
        return self