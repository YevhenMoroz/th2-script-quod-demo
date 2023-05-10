from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiModifyClientMessage(RestApiMessages):
    def __init__(self, data_set: BaseDataSet):
        super().__init__("", data_set)
        self.message_type = "ModifyAccountGroup"

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
        if agent_fee_for_route: self.change_params({"routeAccountGroup": [
                {
                    "routeID": "24",
                    "routeActGrpName": "CLIENT_COMM_1_EUREX",
                    "agentFeeExemption": "true"
                }
            ]})
        self.set_params(base_parameters)
        return self


