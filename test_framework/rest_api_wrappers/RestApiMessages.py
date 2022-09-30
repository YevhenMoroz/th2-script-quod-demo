from test_framework.data_sets.base_data_set import BaseDataSet


class RestApiMessages:

    def __init__(self, message_type=None, data_set: BaseDataSet = None):
        self.parameters = dict()
        self.message_type = message_type
        self.data_set = data_set

    def get_message_type(self):
        return self.message_type

    def get_parameters(self):
        return self.parameters

    def get_parameter(self, parameter_name: str):
        return self.parameters[parameter_name]

    def update_parameters(self, parameters: dict):
        """
        Universal method for adding and/or updating parameters
        Can take a list of parameters: {'ParameterName_1':'Value',...,'ParameterName_N':'Value'}
        """
        self.parameters.update(parameters)
        return self

    def set_params(self, params: dict):
        """
        Method for setting ready dictionary as message parameters
        """
        self.parameters = params
        return self

    def remove_parameter(self, parameter_name: str):
        """
        Method for removing parameter from message
        """
        self.parameters.pop(parameter_name)
        return self

    def remove_parameters(self, parameter_name_list: list):
        """
        Method for removing list of parameter from message
        """
        for par in parameter_name_list:
            self.parameters.pop(par)
        return self

    def add_value_to_component(self, component_name, values_list):
        """
        Method for adding new values to the component of message
        value_list = [{'ParameterName_1':'Value'},...,{'ParameterName_N':'Value'}] or
        value_list = {'ParameterName_1':'Value'} for single value
        """
        if type(values_list) is list:
            for item in values_list:
                self.parameters[str(component_name)].append(item)
        else:
            self.parameters[str(component_name)].append(values_list)
        return self

    def update_value_in_component(self, component_name, key_in_component, new_value, condition: dict = None):
        """
        Method for updating value in component with optional condition
        Condition format: condition = {'ConditionKey': 'ConditionValue'}
        In case of multiple values in condition:
        condition = {'ConditionKey_1': 'ConditionValue',...,'ConditionKey_N': 'ConditionValue'}
        Will implement OR logic, e.g. it will update value if any of the conditions is TRUE
        """
        for item in self.parameters[component_name]:
            if condition is None:
                item.update({key_in_component: new_value})
            else:
                for key in condition.keys():
                    if item[key] == condition[key]:
                        item.update({key_in_component: new_value})
        return self

    def remove_value_from_component(self, component_name, condition_dict: dict):
        """
        Method for removing values from component
        """
        for i in len(self.parameters[component_name]):
            for key, value in condition_dict.items():
                if self.parameters[component_name][i][key] == value:
                    self.parameters[component_name][i] = None
                    break
        return self

    def remove_field_from_component(self, component_name, field_name):
        """
        Method for removing fields from components
        """
        for i in self.parameters[component_name]:
            if field_name in i.keys():
                i.pop(field_name)

    def clear_component(self, component_name):
        """
        Method for clearing the whole component
        """
        if component_name in self.parameters.keys():
            self.parameters[component_name] = []
        return self

    def add_component(self, component_name):
        """
        Method for setting up new empty component in message
        """
        self.parameters.update({component_name: []})

    def clear_message_params(self):
        """
        Method for clearing parameters of message
        """
        self.parameters = None
        return self

    def clear_message_type(self):
        """
        Method for clearing type of message
        """
        self.message_type = None
        return self

    def clear_message(self):
        """
        Method for clearing message
        """
        self.message_type = None
        self.parameters = None
        return self

    def change_params(self, param_modify: dict):
        """
        Method for changing parameters in message
        """
        for key, value in param_modify.items():
            self.parameters[key] = value
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

    def drop_session(self, user_id, role_id, session_key):
        self.message_type = "DropSession"
        drop_session_params = {
            "dropSessionElement": [
                {
                    "userID": user_id,
                    "roleID": role_id,
                    "sessionKey": session_key
                }
            ]
        }
        self.parameters = drop_session_params

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

    def create_security_account(self, params):
        self.message_type = "CreateSecurityAccount"
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

    def send_user_feedback(self, params):
        self.message_type = 'SendUserFeedback'
        self.parameters = params

    def create_wash_book_rule(self, params):
        self.message_type = "CreateWashBookRule"
        self.parameters = params

    def modify_wash_book_rule(self, params):
        self.message_type = "ModifyWashBookRule"
        self.parameters = params

    def delete_wash_book_rule(self, wash_book_rule_id):
        self.message_type = "DeleteWashBookRule"
        delete_params = {
            'washBookRuleID': int(wash_book_rule_id),
        }
        self.parameters = delete_params

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

    def find_all_user_session(self):
        self.message_type = "FindAllUserSession"

    def find_all_client(self):
        self.message_type = "FindAllAccountGroup"

    def find_all_client_tier(self):
        self.message_type = 'FindAllClientTier'

    def find_all_client_tier_instr(self):
        self.message_type = 'FindAllClientTierInstrSymbol'
