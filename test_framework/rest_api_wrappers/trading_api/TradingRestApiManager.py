import logging
from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from google.protobuf.json_format import MessageToDict
from th2_grpc_common.common_pb2 import ConnectionID
from custom.basic_custom_actions import wrap_message
from stubs import Stubs
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import ExpectedMessage, \
    SubmitMessageMultipleResponseRequest


class TradingRestApiManager:
    def __init__(self, session_alias_http, session_alias_web_socket=None, case_id=None):
        self.act = Stubs.api_service
        self.session_alias_http = session_alias_http
        self.session_alias_web_socket = session_alias_web_socket
        self.case_id = case_id

    def send_http_request_and_receive_http_response(self, trd_api_message):
        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(content=trd_api_message.get_parameters(),
                                 message_type=trd_api_message.get_request_type_http(),
                                 session_alias=self.session_alias_http),
            parent_event_id=self.case_id,
            description=f"Send http request and get http response",
            expected_messages=[
                ExpectedMessage(
                    message_type=trd_api_message.get_response_type_http(),
                    key_fields=trd_api_message.key_fields_http_response,
                    connection_id=ConnectionID(session_alias=self.session_alias_http)
                ),
            ]
        )
        message = Stubs.api_service.submitMessageWithMultipleResponse(request)

        return message

    def send_http_request_and_receive_websocket_response(self, trd_api_message: TradingRestApiMessage):

        request = SubmitMessageMultipleResponseRequest(
            message=wrap_message(content=trd_api_message.get_parameters(),
                                 message_type=trd_api_message.get_request_type_http(),
                                 session_alias=self.session_alias_http),
            parent_event_id=self.case_id,
            description=f"Send http request and get two responses: http and web_socket",
            expected_messages=[
                # ExpectedMessage(
                #     message_type=trd_api_message.get_response_type_http(),
                #     key_fields=trd_api_message.key_fields_http_response,
                #     connection_id=ConnectionID(session_alias=self.session_alias_http)
                # ),

                ExpectedMessage(
                    message_type=trd_api_message.get_message_type_web_socket(),
                    key_fields=trd_api_message.key_fields_web_socket_response,
                    connection_id=ConnectionID(session_alias=self.session_alias_web_socket)
                )

            ]
        )
        message = Stubs.api_service.submitMessageWithMultipleResponse(request)

        return message

    @staticmethod
    def parse_response_details(response):
        try:
            response_to_dict = MessageToDict(response)  # Convert grpc message to dictionary
            fields_data = dict()
            fields_name = []
            for data in response_to_dict['responseMessage']:
                for message in data:
                    if message == 'fields':
                        for key, value in data['fields'].items():
                            fields_name.append(key)
                            if 'simpleValue' in value.keys():
                                if value['simpleValue'] == 'PendingOpen':
                                    pass
                                else:
                                    fields_data.update({key: value['simpleValue']})
                            if 'messageValue' in value.keys():
                                for message_key, message_value in value['messageValue']['fields'].items():
                                    fields_data.update({message_key: message_value['simpleValue']})
                            elif 'listValue' in value.keys():
                                for list_values in value['listValue']['values']:
                                    for list_key, list_value in list_values['messageValue']['fields'].items():
                                        if 'simpleValue' in list_value.keys():
                                            fields_data.update({list_key: list_value['simpleValue']})
            fields_data.update({'fields_name': fields_name})
            return fields_data
        except Exception:
            logging.error("Error parsing", exc_info=True)

    @staticmethod
    def parse_response_details_repeating_group(response):
        try:
            response_to_dict = MessageToDict(response)  # Convert grpc message to dictionary
            fields_data_list = list()
            fields_data_dict = dict()
            fields_name = list()

            for data in response_to_dict['responseMessage']:
                for message in data:
                    if message == 'fields':
                        for key, value in data['fields'].items():
                            fields_name.append(key)
                            if 'simpleValue' in value.keys():
                                fields_data_dict.update({key: value['simpleValue']})
                            elif 'listValue' in value.keys():
                                for list_values in value['listValue']['values']:
                                    temp_dict = dict()
                                    for list_key, list_value in list_values['messageValue']['fields'].items():
                                        if 'simpleValue' in list_value.keys():
                                            temp_dict.update({list_key: list_value['simpleValue']})
                                        elif 'listValue' in list_value.keys():
                                            for sub_list_values in list_value['listValue']['values']:
                                                for sub_list_key, sub_list_value in sub_list_values['messageValue'][
                                                    'fields'].items():
                                                    temp_dict.update({sub_list_key: sub_list_value['simpleValue']})
                                    fields_data_list.append(temp_dict)
            fields_data_dict.update({'fields_name': fields_name})
            fields_data_list.append(fields_data_dict)
            return fields_data_list

        except Exception:
            logging.error("Error parsing", exc_info=True)
