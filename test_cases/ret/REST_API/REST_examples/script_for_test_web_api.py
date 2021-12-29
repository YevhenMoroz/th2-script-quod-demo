import logging
import os

from th2_grpc_act_gui_quod.ar_operations_pb2 import ExtractOrderTicketValuesRequest, ExtractDirectVenueExecutionRequest
from th2_grpc_common.common_pb2 import Direction

from custom.basic_custom_actions import timestamps, convert_to_get_request, wrap_message
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ContextActionType
from win_gui_modules.application_wrappers import CloseApplicationRequest
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call, close_fe, prepare_fe
from test_framework.old_wrappers.ret_wrappers import enable_gating_rule, disable_gating_rule
from test_framework.old_wrappers.web_rest_wrappers import WebAdminRestMessage


def modify_gating_rule(case_id, gating_rule_id):
    api = Stubs.api_service
    modify_params = {
        "accountGroupID": "HAKKIM",
        "userID": "QA3",
        "gatingRuleDescription": "to manage DMA orders",
        "gatingRuleName": "QAP-4307(Gr_for_DMA)",
        "gatingRuleID": gating_rule_id,
        "gatingRuleCondition": [
            {
                "gatingRuleCondExp": "AND(ExecutionPolicy=DMA,OrdQty<1000)",
                "gatingRuleCondName": "DMATinyQty",
                "holdOrder": "true",
                "qtyPrecision": 100,
                "alive": "true",
                "gatingRuleCondIndice": 1,
                "gatingRuleResult": [
                    {
                        "alive": "true",
                        "gatingRuleResultIndice": 1,
                        "splitRatio": 1,
                        "gatingRuleExecPolicyResult": "DMA"
                    }
                ]
            },
            {
                "gatingRuleCondName": "DMADefResult",
                "alive": "null",
                "gatingRuleCondIndice": 2,
                "gatingRuleResult": [
                    {
                        "alive": "true",
                        "gatingRuleResultIndice": 1,
                        "splitRatio": 1,
                        "gatingRuleExecPolicyResult": "DMA"
                    }
                ]
            }
        ]
    }
    api.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=modify_params,
                                                                          message_type='ModifyGatingRule',
                                                                          session_alias='rest_wa315luna'),
                                                 parent_event_id=case_id))
    print(modify_params)
    return modify_params


def modify_user(case_id):
    api = Stubs.api_service

    modify_message = {
        "userConfirmFollowUp": "false",
        "userID": "adm_rest",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "headOfDesk": "false",
    }
    api.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=modify_message,
                                                                          message_type='ModifyUser',
                                                                          session_alias='rest_wa315luna'),
                                                 parent_event_id=case_id))


def enable_client(case_id, act):
    enable_client = {

        "accountGroupID": "POOJA",

    }
    act.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=enable_client,
                                                                          message_type='EnableAccountGroup',
                                                                          session_alias='rest_wa315luna'),
                                                 parent_event_id=case_id))


def disable_client(case_id, act):
    disable_client = {

        "accountGroupID": "POOJA",

    }
    act.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=disable_client,
                                                                          message_type='DisableAccountGroup',
                                                                          session_alias='rest_wa315luna'),
                                                 parent_event_id=case_id))


def create_client(case_id, act):
    create_client = {

        "accountGroupName": "test_api_client3",
        "clientAccountGroupID": "test_api_client3",
        "accountGroupID": "test_api_client3",
        "accountType": "HT",
        "accountScheme": "S",
        "transactionType": "C",
        "discloseExec": "M",
        "clearingAccountType": "FIR",
        "allocationInst": "MAN"
    }
    act.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=create_client,
                                                                          message_type='CreateAccountGroup',
                                                                          session_alias='rest_wa315luna'),

                                                 parent_event_id=case_id))
    # test_request = convert_to_get_request("test",
    #                                       'rest_wa315luna',
    #                                       case_id,
    #                                       wrap_message({}, "CreateAccountGroup", 'rest_wa315luna'),
    #                                       "FindAllAccountGroup",
    #                                       "FindAllAccountGroupReply")
    # response = Stubs.api_service.sendGetRequest(test_request)
    # print(response.response_message)


def execute(report_id):
    act = Stubs.api_service

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    # requests

    #enable_client(case_id, act)
    #disable_client(case_id, act)
    create_client(case_id, act)
    #modify_user(case_id)
    # get_request(case_id)
    # enable_gating_rule(case_id, gating_rule_id=1)
    # disable_gating_rule(case_id, gating_rule_id=1)
    # activate_gating_rule(case_id, gating_rule_id=1, gating_rule_name="QAP-4288(Gr_for_Care)")
    # rest_message = modify_gating_rule(case_id, gating_rule_id=1)
    # new_message = WebAdminRestMessage(rest_message)
    # new_message.change_parameters({'userID': 'QA2'})
    # amend_request = api.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=rest_message,
    #                                                                                       message_type='ModifyGatingRule',
    #                                                                                       session_alias='rest_wa315luna'),
    #                                                              parent_event_id=case_id))
