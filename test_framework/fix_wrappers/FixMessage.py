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

    def change_parameter(self, parameter_name: str, new_parameter_value) -> None:
        self.__parameters[parameter_name] = new_parameter_value

    def change_parameters(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.__parameters[key] = parameter_list[key]
        return self

    def add_tag(self, parameter: dict):
        self.__parameters.update(parameter)
        return self

    def remove_parameter(self, parameter_name: str):
        self.__parameters.pop(parameter_name)
        return self

    def add_ClordId(self, test_case_name):
        self.change_parameter("ClOrdID", test_case_name + " " + basic_custom_actions.client_orderid(9))
        return self

    def print_parameters(self) -> None:
        # TODO
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

    def add_fields_into_repeating_group(self, r_group: str, fields: list):
        if r_group in self.get_parameters():
            new_component = self.get_parameter(r_group)
            for i in fields:
                new_component.append(i)
            self.change_parameters({r_group: new_component})
        else:
            self.add_tag({r_group: fields})
        return self


    def remove_fields_repeating_group(self, r_group: str, fields: list):
        new_component = self.get_parameter(r_group)
        ln = len(new_component)
        for i in range(0, ln):
            for j in fields:
                if new_component[i] == j:
                    new_component.pop(i)

        self.change_parameters({r_group: new_component})
        return self
