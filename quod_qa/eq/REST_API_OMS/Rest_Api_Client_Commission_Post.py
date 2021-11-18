from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitGetMessageRequest, SubmitMessageRequest
from custom import basic_custom_actions as bca
from quod_qa.wrapper.RestApiManager import RestApiManager
from quod_qa.wrapper.RestApiMessages import RestApiMessages
from stubs import Stubs
from custom.basic_custom_actions import create_event, wrap_message, convert_to_request, create_check_rule, wrap_filter, \
    convert_to_get_request


def execute(report_id):
    case_id = create_event("modify fees ", report_id)
    session_alias = "rest_wa317ganymede"

    rest = RestApiMessages()
    rest.modify_client_commission_request()
    rest.change_params_for_fees_modify_request({'commissionProfileID': 6})
    rest_manager = RestApiManager(session_alias, case_id)
    print(rest.parameters)
    rest_manager.send_post_request(rest)
