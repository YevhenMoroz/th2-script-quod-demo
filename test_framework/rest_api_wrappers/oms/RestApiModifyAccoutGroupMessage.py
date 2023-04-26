from test_framework.environments.full_environment import FullEnvironment
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiModifyAccountGroupMessage(RestApiMessages):
    def __init__(self, data_set, enviroment: FullEnvironment):
        super().__init__("", data_set)
        self.message_type = "ModifyAccountGroup"
        self._base_parametes = {"accountGroupName": "CLIENT_REST_API",
                                "clientAccountGroupID": "CLIENT_REST_API",
                                "accountGroupID": "CLIENT_REST_API",
                                "accountType": "AC",
                                "FIXOrderRecipientUserID": "JavaApiUser",
                                "FIXOrderRecipientRoleID": "TRA",
                                "accountScheme": "S", "transactionType": "C",
                                "accountGroupDesc": "",
                                "FIXOrderRecipientDeskID": enviroment.get_list_fe_environment()[0].desk_ids[0],
                                "discloseExec": "R",
                                "clearingAccountType": "INS",
                                "bookingInst": "AUT",
                                "middleOfficeDeskID":  enviroment.get_list_fe_environment()[0].desk_ids[1],
                                "allocationInst": "AUT",
                                "confirmationService": "MAN",
                                "blockApproval": "AUT",
                                "pxPrecision": '3',
                                "roundingDirection": "RDO",
                                "giveUpMatchingID": "CLIENT_REST_API",
                                "orderAckPreference": "AUT",
                                "venueAccountGroup": [{"venueClientActGrpName": "CLIENT_REST_API", "venueID": "EUREX",
                                                       "venueActGrpName": "CLIENT_REST_API", "stampFeeExemption": 'false',
                                                       "levyFeeExemption": 'false', "perTransacFeeExemption": 'false'}],
                                "routeAccountGroup": [
                                    {"routeID": self.data_set.get_route_id_by_name('route_1'), "routeActGrpName": "CLIENT_REST_API", "agentFeeExemption": 'true'}],
                                "managerDesk": [{"deskID": enviroment.get_list_fe_environment()[0].desk_ids[1]}]}

    def set_default(self):
        self.parameters.update(self._base_parametes)
