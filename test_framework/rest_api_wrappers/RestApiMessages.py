from test_framework.fix_wrappers.DataSet import FeesAndCommissions, CommissionAccounts, \
    CommissionClients


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

    def change_parameter(self, parameter_name: str, new_parameter_value):
        self.parameters[parameter_name] = new_parameter_value
        return self

    def change_parameters(self, parameter_list: dict):
        if parameter_list is not None:
            for key in parameter_list:
                self.parameters[key] = parameter_list[key]
        return self

    def add_parameter(self, parameter: dict):
        self.parameters.update(parameter)
        return self

    def remove_parameter(self, parameter_name: str):
        self.parameters.pop(parameter_name)
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

    def modify_client_tier_instrument(self, params):
        self.parameters = params
        self.message_type = 'ModifyClientTierInstrSymbol'

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

    def find_all_client_tier_instr(self):
        self.message_type = 'FindAllClientTierInstrSymbol'

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

    def change_params(self, param_modify: dict):
        for key, value in param_modify.items():
            self.parameters[key] = value
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
