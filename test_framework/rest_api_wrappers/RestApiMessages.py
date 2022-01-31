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
            if key_in_component in item.keys():
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

    def modify_fees_request(self, params=None, recalculate=False, fee: FeesAndCommissions = None):
        self.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': "Fee1" if fee is None else fee.name,
            'commExecScope': "ALL",
            'commissionID': 1 if fee is None else fee.value,
            'execCommissionProfileID': 1,
            'miscFeeType': 'EXC',
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
        }
        self.parameters = params if params is not None else default_parameters
        return self

    def clear_fees_request(self, commission_id):
        self.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': "FeeCleared",
            'commissionID': commission_id,
            'miscFeeType': 'EXC'
        }
        self.parameters = default_parameters
        return self

    def modify_client_commission_request(self, params=None, client: CommissionClients = None,
                                         account: CommissionAccounts = None, recalculate=False,
                                         commission: FeesAndCommissions = None):
        self.message_type = 'ModifyClCommission'
        default_parameters = {
            'accountGroupID': "CLIENT_COMM_1" if client is None else client.value,
            'clCommissionDescription': "Commission of Testing MOClient",
            'clCommissionID': 1 if commission is None else commission.value,
            'clCommissionName': "Commission1" if commission is None else commission.name,
            'commissionAmountType': "BRK",
            'commissionProfileID': 1,
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
            'venueID': "EUREX"
        }
        if account is not None and client is None:
            default_parameters.pop("accountGroupID")
            default_parameters["accountID"] = account.value
        self.parameters = params if params is not None else default_parameters
        return self

