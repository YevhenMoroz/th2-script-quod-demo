from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet


class FixMessage:

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

    def add_tag(self, parameter: dict):
        self.__parameters.update(parameter)
        return self

    def remove_parameter(self, parameter_name: str):
        self.__parameters.pop(parameter_name)
        return self

    def remove_parameters(self, parameter_name_list: list):
        for par in parameter_name_list:
            self.__parameters.pop(par)
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

    def update_repeating_group(self, r_group: str, fields: list):
        self.remove_parameter(r_group)
        self.add_fields_into_repeating_group(r_group, fields)
        return self

    def add_fields_into_repeating_group_algo(self, r_group: str, fields: list):
        params = ['StrategyParameterName', 'StrategyParameterType', 'StrategyParameterValue']
        if r_group in self.get_parameters() and r_group !='NoStrategyParameters':
            new_component = self.get_parameter(r_group)
            for i in fields:
                new_component.append(i)
            self.change_parameters({r_group: new_component})
        if r_group in self.get_parameters() and r_group == 'NoStrategyParameters':
            new_component = self.get_parameter(r_group)
            for i in fields:
                new_component.append(dict(zip(params, i)))
            self.change_parameters({r_group: new_component})
        else:
            fields_l = []
            for i in fields:
                fields_l.append(dict(zip(params, i)))
            self.add_tag({r_group: fields_l})
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

    def remove_fields_in_repeating_group(self, r_group: str, fields: list):
        """
        Removing list of fields from repeating group, for example we can delete Side from this msg
        {
        "NoRelatedSymbols": [{
                "Account": "Iridium1",
                "Side": "1",
                "OrderQty": "1000000",
                "Instrument": {
                    "Symbol": "GBP/USD",
                    "SecurityType": "FXSWAP"
                }]
        }
        fix_message.remove_fields_in_repeating_group("NoRelatedSymbols", ["Side"])
        """
        new_repeating_gr = self.get_parameter(r_group)
        for element in new_repeating_gr:
            for i in fields:
                if i in element.keys():
                    del element[i]
        self.change_parameters({r_group: new_repeating_gr})
        return self

    def update_value_in_repeating_group(self, r_group, key_in_group, new_value):
        for item in self.__parameters[r_group]:
            if key_in_group in item.keys():
                item.update({key_in_group: new_value})
        return self

    def update_repeating_group_by_index(self, component: str, index: int = 0, **kwargs):
        new_component = self.get_parameter(component)
        new_component[index].update(kwargs)
        return self

    def remove_values_in_repeating_group_by_index(self, component: str, index: int = 0, *args: tuple):
        """
        Removing list of values from repeating group by index, for example
        we can delete MDEntryPx and MDEntryTime from this msg:
        {'MDReqID': '0289630222', ..., 'Instrument': {'Symbol': 'EUR/USD'},
        'NoMDEntries': [
        {'SettlType': '0', 'MDEntryPx': '*', 'MDEntryTime': '*', ..., 'SettlDate': '20220815'},
        {'SettlType': '0', 'MDEntryPx': '*', 'MDEntryTime': '*', ..., 'SettlDate': '20220815'}
        ]}
        fix_message.remove_values_in_repeating_group_by_index("NoMDEntries", 1, ("MDEntryPx", "MDEntryTime"))
        """
        new_repeating_gr = self.get_parameter(component)
        for i in args[0]:
            new_repeating_gr[index].pop(i)
        return self

    def get_data_set(self):
        return self.__data_set

    def delete_group(self, field):
        del self.__parameters[field]
