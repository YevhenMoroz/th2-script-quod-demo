from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message, create_event
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd


class TestCase:
    def __init__(self, report_id, ):
        self.case_id = bca.create_event("QAP_6401", report_id)
        self.api = Stubs.act_rest
        self.http = 'rest_wt320kuiper'

    def send_order_archive_request(self):
        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(content={'URI': {
                "StartTime": "2022-02-09T00:00:00",
                "EndTime": "2022-02-10T23:59:59"
            }},
                                 message_type='OrderArchiveMassStatusRequest',
                                 session_alias=self.http),
            parent_event_id=self.case_id,
            description="Send OrderArchiveMassStatusRequest",
            expected_messages=[

                ExpectedMessage(
                    message_type='OrderArchiveMassStatusRequestReply',
                    key_fields={"ReplyType": "Accepted"},
                    connection_id=
                    ConnectionID(session_alias=self.http)
                )

            ]
        )
        messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
        print(messages)

    def execute(self):
        self.send_order_archive_request()

