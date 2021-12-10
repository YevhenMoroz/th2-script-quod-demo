from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message, create_event
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime


def execute(report_id):
    case_id = create_event("test", report_id)
    api = Stubs.act_rest
    trading_conn = 'trading_ret'
    ws_conn = 'api_session_ret'
    api_message = RestApiMessages()
    api_manager = RestApiManager(session_alias='rest_wa315luna', case_id=case_id)

    position_params = {
        "ClientPosReqID": bca.client_orderid(9),
        "PosReqType": "Positions",
        "SubscriptionRequestType": "Snapshot",
        "Parties": [
            {
                "PartyID": "POOJA",
                "PartyIDSource": "BIC",
                "PartyRole": "PositionAccount"
            }
        ]
    }

    position_request = SubmitMessageMultipleResponseRequest(
        message=wrap_message(position_params, 'PositionRequest', trading_conn),
        parent_event_id=case_id,
        description="Send PositionRequest",
        expected_messages=[

            ExpectedMessage(
                message_type='PositionReport',
                key_fields={},
                connection_id=ConnectionID(session_alias=ws_conn)
            )
        ]
    )
    messages = Stubs.api_service.submitMessageWithMultipleResponse(position_request).response_message
    print(messages)