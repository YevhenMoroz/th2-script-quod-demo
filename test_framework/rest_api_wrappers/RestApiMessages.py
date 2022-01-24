class RestApiMessages:

    def __init__(self, message_type: str = ''):
        self.parameters = dict()
        self.message_type = message_type

    def get_message_type(self):
        return self.message_type

    def get_parameters(self):
        return self.parameters

    def get_parameter(self, parameter_name: str):
        return self.parameters[parameter_name]

    def update_parameters(self, parameters: dict):  #
        self.parameters.update(parameters)          # Universal method fro adding new parameters
        return self                                 # and also updating existing

    def set_params(self, params: dict):
        self.parameters = params
        return self

    def remove_parameter(self, parameter_name: str):
        self.parameters.pop(parameter_name)
        return self

    def add_value_to_component(self, component_name, values_list):
        if type(values_list) is list:
            for item in values_list:
                self.parameters[str(component_name)].append(item)
        else:
            self.parameters[str(component_name)].append(values_list)
        return self

    def update_value_in_component(self, component_name, key_in_component, new_value, condition=None):
        for item in self.parameters[component_name]:
            if key_in_component in item.keys():
                if condition is None:
                    item.update({key_in_component, new_value})
                elif item[key_in_component] == condition:
                    item.update({key_in_component, new_value})
        return self

    def remove_value_from_component(self, component_name, condition_dict: dict):
        for i in len(self.parameters[component_name]):
            for key, value in condition_dict.items():
                if self.parameters[component_name][i][key] == value:
                    self.parameters[component_name][i] = None
                    break

    def clear_component(self, component_name):
        if component_name in self.parameters.keys():
            self.parameters[component_name] = []
        return self

    def add_component(self, component_name):
        self.parameters.update({component_name: []})

    def clear_params(self):
        self.parameters = None
        return self

    def modify_user_to_site(self):
        self.message_type = "ModifyUser"
        modify_params = {
            "userConfirmFollowUp": "false",
            "userID": "adm_rest",
            "useOneTimePasswd": "false",
            "pingRequired": "false",
            "generatePassword": "false",
            "generatePINCode": "false",
            "headOfDesk": "false",
        }
        self.parameters = modify_params

    def create_institution(self, params):
        self.message_type = "CreateInstitution"
        self.parameters = params

    def modify_venue_status_metric(self, venue,
                                   status: str = 'false',
                                   error_threshold: int = -1,
                                   warning_threshold: int = 25):
        self.message_type = 'ModifyVenueStatus'
        modify_params = {
            'alive': 'true',
            'venueID': venue,
            'venueStatusMetric': [
                {
                    'venueMetricType': "LUP",
                    'enableMetric': status,
                    'metricErrorThreshold': error_threshold,
                    'metricWarningThreshold': warning_threshold
                }
            ]
        }
        self.parameters = modify_params

    def modify_institution(self, params):
        self.message_type = "ModifyInstitution"
        self.parameters = params

    def modify_user(self, params):
        self.message_type = "ModifyUser"
        self.parameters = params

    def enable_gating_rule(self, gating_rule_id):
        self.message_type = "EnableGatingRule"

        enable_params = {
            "gatingRuleID": gating_rule_id,
        }
        self.parameters = enable_params

    def disable_gating_rule(self, gating_rule_id):
        self.message_type = "DisableGatingRule"

        disable_params = {
            "gatingRuleID": gating_rule_id,
        }
        self.parameters = disable_params

    def modify_gating_rule(self, params):
        self.message_type = "ModifyGatingRule"
        self.parameters = params

    def create_client(self, params):
        self.message_type = "CreateAccountGroup"
        self.parameters = params

    def modify_client(self, params):
        self.message_type = "ModifyAccountGroup"
        self.parameters = params

    def enable_client(self, client_id):
        self.message_type = "EnableAccountGroup"

        enable_params = {
            "accountGroupID": client_id,
        }
        self.parameters = enable_params

    def disable_client(self, client_id):
        self.message_type = "DisableAccountGroup"

        disable_params = {
            "accountGroupID": client_id,
        }
        self.parameters = disable_params

    def find_all_institution(self):
        self.message_type = "FindAllInstitution"

    def find_all_zone(self):
        self.message_type = "FindAllZone"

    def find_all_location(self):
        self.message_type = "FindAllLocation"

    def find_all_desk(self):
        self.message_type = "FindAllDesk"

    def find_all_user(self):
        self.message_type = "FindAllUser"

    def find_all_client(self):
        self.message_type = "FindAllAccountGroup"

    def find_all_client_tier(self):
        self.message_type = 'FindAllClientTier'

    def change_params(self, param_modify: dict):
        for key, value in param_modify.items():
            self.parameters[key] = value
        return self

    def find_all_client_tier_instr(self):
        self.message_type = 'FindAllClientTierInstrSymbol'
