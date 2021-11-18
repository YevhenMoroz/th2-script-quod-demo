class RestApiMessages:

    def __init__(self):
        self.parameters = ""
        self.message_type = ""

    def get_message_type(self):
        return self.message_type

    def get_parameters(self):
        return self.parameters

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

    def modify_fees_request(self, params=None, recalculate=False):
        self.message_type = 'ModifyCommission'
        default_parameters = {
            'commDescription': "FeeDescription",
            'commExecScope': "ALL",
            'commissionID': 1,
            'execCommissionProfileID': 200013,
            'miscFeeType': 'EXC',
            'recomputeInConfirmation': 'false' if recalculate is False else 'true',
            'venueID': "EUREX"
        }
        self.parameters = params if params is not None else default_parameters
        return self

    def change_params(self, param_modify: dict):
        for key, value in param_modify.items():
            self.parameters[key] = value
        return self

    def modify_client_commission_request(self, params=None):
        self.message_type = 'ModifyClCommission'
        default_parameters = {
            'accountGroupID': "CLIENT_COMM_1",
            'clCommissionDescription': "Commission of Testing MOClient",
            'clCommissionID': 1000008,
            'clCommissionName': "Commission_for_MOClient",
            'commissionAmountType': "BRK",
            'commissionProfileID': 6,
            'recomputeInConfirmation': 'false',
            'venueID': "EUREX"
        }
        self.parameters = params if params is not None else default_parameters
