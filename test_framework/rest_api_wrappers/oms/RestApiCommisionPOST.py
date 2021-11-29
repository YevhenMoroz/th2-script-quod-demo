from custom.basic_custom_actions import create_event
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


def execute(report_id):
    case_id = create_event("modify fees ", report_id)
    session_alias = "rest_wa317ganymede"

    rest = RestApiMessages()
    rest.modify_client_commission_request()
    rest.change_params_for_fees_modify_request({'commissionProfileID': 6})
    rest_manager = RestApiManager(session_alias, case_id)
    print(rest.parameters)
    rest_manager.send_post_request(rest)
