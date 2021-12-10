from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitGetMessageRequest
from custom import basic_custom_actions as bca
from stubs import Stubs
from custom.basic_custom_actions import create_event, wrap_message, convert_to_request, create_check_rule, wrap_filter, \
    convert_to_get_request


def execute(report_id):
    case_id = create_event("dz test", report_id)
    session_alias = "rest_wa315luna"

    # request = convert_to_request(
    #     "Send GET request",
    #     session_alias,
    #     case_id,
    #     wrap_message({}, "FindAllLocation", session_alias)
    # )
    response_fields = {
        'LocationResponse': [
            {
                "locationName": "Kharkiv",
                "zoneID": 1,
                "locationID": 1,
                "alive": 1
            }
        ]
    }
    test_request = convert_to_get_request("test",
                                          session_alias,
                                          case_id,
                                          wrap_message({}, "FindAllZone", session_alias),
                                          "FindAllZone",
                                          "FindAllZoneReply")

    response = Stubs.api_service.sendGetRequest(test_request)
    print(response.response_message)
    checkpoint_1 = response.checkpoint_id
    Stubs.verifier.submitCheckRule(
        request=create_check_rule(
            "Check FindAllLocationReply",
            wrap_filter(response_fields, "FindAllLocationReply"),
            checkpoint_1, session_alias, case_id
        )
    )
    Stubs.factory.close()