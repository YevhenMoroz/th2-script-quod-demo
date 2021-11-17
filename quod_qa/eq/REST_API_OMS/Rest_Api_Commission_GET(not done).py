from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitGetMessageRequest
from custom import basic_custom_actions as bca
from stubs import Stubs
from custom.basic_custom_actions import create_event, wrap_message, convert_to_request, create_check_rule, wrap_filter, \
    convert_to_get_request


def execute(report_id):
    case_id = create_event("dz test", report_id)
    session_alias = "rest_wa317ganymede"

    # request = convert_to_request(
    #     "Send GET request",
    #     session_alias,
    #     case_id,
    #     wrap_message({}, "FindAllLocation", session_alias)
    # )

    test_request = convert_to_get_request("test",
                                          session_alias,
                                          case_id,
                                          wrap_message({}, "FindAllClCommission", session_alias),
                                          "FindAllClCommission",
                                          "FindAllClCommissionReply")
    response = Stubs.api_service.sendGetRequest(test_request)
    print(response.response_message)
