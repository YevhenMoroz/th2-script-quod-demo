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
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)
    #
    # api_message.enable_gating_rule(gating_rule_id=1)
    # api_manager.send_post_request(api_message=api_message)
    #
    # api_message.disable_gating_rule(gating_rule_id=1)
    # api_manager.send_post_request(api_message=api_message)

    # create_params = {
    #     "accountMgrUserID": "QA2",
    #     "accountGroupName": "test_api_client3",
    #     "accountMgrDeskID": 5,
    #     "clientAccountGroupID": "test_client",
    #     "accountGroupID": "test_api_client3",
    #     "accountType": "HT",
    #     "accountScheme": "S",
    #     "transactionType": "C",
    #     "discloseExec": "M",
    #     "accountMgrRoleID": "HSD",
    #     "clearingAccountType": "FIR",
    #     "allocationInst": "MAN"
    # }
    # api_message.create_client(create_params)
    # api_manager.send_post_request(api_message=api_message)
    # api_message.find_all_client()
    # response = api_manager.send_get_request(api_message=api_message)
    # #print(response)

    # api_message.find_all_client()
    # client_response = api_manager.send_get_request(api_message=api_message)
    # # print(client_response.fields["AccountGroupResponse"].list_value.values[0].message_value.fields)
    # parsed_response = api_manager.get_response_details(response=client_response,
    #                                                    response_name="AccountGroupResponse",
    #                                                    expected_entity_name="TestClient(QAP_4316)",
    #                                                    entity_field_id="accountGroupID")
    # print(parsed_response)
    #
    # print(parsed_response["alive"].simple_value)
    # print(api_manager.get_response_multiple_details(response=client_response,
    #                                                 response_name="AccountGroupResponse",
    #                                                 entity_field_id="accountGroupID",
    #                                                 field_name="alive"))
    # api_message.find_all_user()
    # user_response = api_manager.send_get_request(api_message=api_message)
    # print(user_response)
    modify_message = {
        "userConfirmFollowUp": "false",
        "userID": "adm_inst",
        "useOneTimePasswd": "false",
        "pingRequired": "false",
        "generatePassword": "false",
        "generatePINCode": "false",
        "zoneID": "1",
        "headOfDesk": "false",
    }
    api_message.modify_user(modify_message)
    api_manager.send_post_request(api_message=api_message)

    # test_request = convert_to_get_request("test",
    #                                       'rest_wa315luna',
    #                                       case_id,
    #                                       wrap_message({}, "FindAllAccountGroup", 'rest_wa315luna'),
    #                                       "FindAllAccountGroup",
    #                                       "FindAllAccountGroupReply")
    #
    # response = Stubs.api_service.sendGetRequest(test_request)
    # print(response.response_message)
