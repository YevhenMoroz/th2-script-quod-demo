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

    def set_params_for_comm_client(self, agent_fee_for_route=False):
        base_parameters = {
            "accountGroupName": "CLIENT_COMM_1",
            "clientAccountGroupID": "CLIENT_COMM_1",
            "accountGroupID": "CLIENT_COMM_1",
            "accountType": "AC",
            "FIXOrderRecipientUserID": "JavaApiUser",
            "FIXOrderRecipientRoleID": "TRA",
            "accountScheme": "S",
            "transactionType": "C",
            "accountGroupDesc": "Client for client commission",
            "FIXOrderRecipientDeskID": "9",
            "discloseExec": "R",
            "clearingAccountType": "INS",
            "bookingInst": "MAN",
            "middleOfficeDeskID": "10",
            "allocationInst": "MAN",
            "confirmationService": "MAN",
            "blockApproval": "MAN",
            "pxPrecision": "3",
            "roundingDirection": "RDO",
            "allocInstructionMisc1": "BOC2",
            "allocInstructionMisc2": "BOC3",
            "allocInstructionMisc3": "BOC4",
            "allocInstructionMisc4": "BOC5",
            "allocInstructionMisc0": "BOC1",
            "giveUpService": "MAN",
            "giveUpMatchingID": "CLIENT_COMM_1",
            "orderAckPreference": "AUT",
            "alive": "true",
            "venueAccountGroup": [
                {
                    "venueID": "CHIX",
                    "venueActGrpName": "CLIENT_COMM_1_CHIX",
                    "stampFeeExemption": "false",
                    "levyFeeExemption": "false",
                    "perTransacFeeExemption": "false"
                },
                {
                    "venueID": "EUREX",
                    "venueActGrpName": "CLIENT_COMM_1_EUREX",
                    "stampFeeExemption": "false",
                    "levyFeeExemption": "false",
                    "perTransacFeeExemption": "false"
                },
                {
                    "venueID": "JSE",
                    "venueActGrpName": "CLIENT_COMM_1_JSE",
                    "stampFeeExemption": "false",
                    "levyFeeExemption": "false",
                    "perTransacFeeExemption": "false"
                },
                {
                    "defaultRouteID": "24",
                    "venueID": "PARIS",
                    "venueActGrpName": "CLIENT_COMM_1_PARIS",
                    "stampFeeExemption": "false",
                    "levyFeeExemption": "false",
                    "perTransacFeeExemption": "false"
                },
                {
                    "venueID": "TRQX",
                    "venueActGrpName": "CLIENT_COMM_1_TRQX",
                    "stampFeeExemption": "false",
                    "levyFeeExemption": "false",
                    "perTransacFeeExemption": "false"
                }
            ],
            "routeAccountGroup": [
                {
                    "routeID": "24",
                    "routeActGrpName": "CLIENT_COMM_1_EUREX",
                    "agentFeeExemption": "false"
                }
            ],
            "managerDesk": [
                {
                    "deskID": '4'
                },
                {
                    "deskID": "10"
                },
                {
                    "deskID": "1"
                },
                {
                    "deskID": "7"
                }
            ]
        }
        self.parameters.update(base_parameters)
        if agent_fee_for_route: self.change_params({"routeAccountGroup": [
                {
                    "routeID": "24",
                    "routeActGrpName": "CLIENT_COMM_1_EUREX",
                    "agentFeeExemption": "true"
                }
            ]})
        return self
