from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitGetMessageRequest, SubmitMessageRequest
from custom import basic_custom_actions as bca
from stubs import Stubs
from custom.basic_custom_actions import create_event, wrap_message, convert_to_request, create_check_rule, wrap_filter, \
    convert_to_get_request


def execute(report_id):
    case_id = create_event("dz test", report_id)
    session_alias = "rest_wa317ganymede"
    act = Stubs.api_service
    # request = convert_to_request(
    #     "Send GET request",
    #     session_alias,
    #     case_id,
    #     wrap_message({}, "FindAllLocation", session_alias)
    # )
    modify_fees_params = {
        'commDescription': "Fee for testVSCHANGE",
        'commExecScope': "DAF",
        'commOrderScope': "DFD",
        'commissionID': 1,
        'contraFirmCounterpartID': 200003,
        'execCommissionProfileID': 3,
        'executionPolicy': "D",
        'instrType': "EQU",
        'miscFeeCategory': "OTH",
        'miscFeeType': "AGE",
        'orderCommissionProfileID': 3,
        'recomputeInConfirmation': 'true',
        'routeID': 24,
        'venueID': "CHIX"
    }
    act.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=modify_fees_params,
                                                                               message_type='ModifyCommission',
                                                                               session_alias=session_alias),
                                                      parent_event_id=case_id))
