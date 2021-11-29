from stubs import Stubs
from custom.basic_custom_actions import create_event, wrap_message, convert_to_get_request


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
