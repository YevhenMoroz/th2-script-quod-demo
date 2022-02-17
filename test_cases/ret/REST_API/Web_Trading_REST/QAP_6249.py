from th2_grpc_common.common_pb2 import ConnectionID

from custom.basic_custom_actions import wrap_message
from test_cases.wrapper.ret_wrappers import verifier
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest, ExpectedMessage, \
    SubmitMessageMultipleResponseRequest
from custom import basic_custom_actions as bca

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta


class TestCase:
    def __init__(self, report_id):
        self.case_id = bca.create_event('QAP_6249', report_id)
        self.api = Stubs.act_rest
        self.http_conn = 'rest_wt320kuiper'
        self.ws_conn = 'api_session_320kuiper'

    def get_venue_list(self):

        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message({}, 'VenueListRequest', self.http_conn),
            parent_event_id=self.case_id,
            description="Send VenueListRequest",
            expected_messages=[

                ExpectedMessage(
                    message_type='VenueListReply',
                    key_fields={},
                    connection_id=
                    ConnectionID(session_alias=self.http_conn)
                )
            ]
        )
        messages = Stubs.api_service.submitMessageWithMultipleResponse(request).response_message
        print(messages)

    # Main method
    def execute(self):
        self.get_venue_list()


if __name__ == '__main__':
    pass
