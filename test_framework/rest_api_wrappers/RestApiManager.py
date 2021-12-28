from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from custom.basic_custom_actions import convert_to_get_request
from stubs import Stubs
from custom import basic_custom_actions as bca
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict


class RestApiManager:

    def __init__(self, session_alias, case_id=None):
        self.act = Stubs.api_service
        self.session_alias = session_alias
        self.case_id = case_id

    def send_post_request(self, api_message: RestApiMessages):
        self.act.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=api_message.get_parameters(),
                                                                                   message_type=api_message.get_message_type(),
                                                                                   session_alias=self.session_alias),
                                                          parent_event_id=self.case_id))

    def send_get_request(self, api_message: RestApiMessages):
        message = convert_to_get_request(description="Send Get request",
                                         connectivity=self.session_alias,
                                         event_id=self.case_id,
                                         message=bca.wrap_message(content={},
                                                                  message_type=api_message.get_message_type(),
                                                                  session_alias=self.session_alias),
                                         request_type=api_message.get_message_type(),
                                         response_type=api_message.get_message_type() + "Reply")
        response = self.act.sendGetRequest(message)
        return response.response_message

    @staticmethod
    def get_response_details(response, expected_entity_name, entity_field_id):
        response_name = list(dict(response.fields).keys())[0]
        for count in range(len(response.fields[response_name].list_value.values)):
            entity = response.fields[response_name].list_value.values[count].message_value.fields[
                entity_field_id].simple_value
            if entity == expected_entity_name:
                return response.fields[response_name].list_value.values[count].message_value.fields

    @staticmethod
    def parse_response_details(response, filter_dict: dict):
        result = dict()
        temp = dict()
        for i in MessageToDict(response)['fields']:
            temp = MessageToDict(response)['fields'][i]['listValue']['values']
        for i in range(len(temp)):
            result.update({i: temp[i]['messageValue']['fields']})
        temp.clear()
        for i in result.keys():
            temp = result[i]
            for key, value in temp.items():
                if 'simpleValue' in value.keys():
                    temp.update({key: value['simpleValue']})
                elif 'listValue' in value.keys():
                    temp_list = []
                    for list_values in value['listValue']['values']:
                        temp_dict = dict()
                        for list_key, list_value in list_values['messageValue']['fields'].items():
                            if 'simpleValue' in list_value.keys():
                                temp_dict.update({list_key: list_value['simpleValue']})
                            elif 'listValue' in list_value.keys():
                                sub_list=[]
                                for sub_list_values in list_value['listValue']['values']:
                                    sub_dict = dict()
                                    for sub_list_key, sub_list_value in sub_list_values['messageValue']['fields'].items():
                                        sub_dict.update({sub_list_key: sub_list_value['simpleValue']})
                                    sub_list.append(sub_dict)
                                temp_dict.update({list_key: sub_list})
                        temp_list.append(temp_dict)
                    temp.update({key: temp_list})
            result.update({i: temp})
        result_filtered = []
        for key in result.keys():
            for filter_key, filter_value in filter_dict:
                if result[key][filter_key] == filter_value:
                    result_filtered.append(result[key])
        return result_filtered

    @staticmethod
    def get_response_multiple_details(response, response_name, entity_field_id, field_name):

        info = {}
        for count in range(len(response.fields[response_name].list_value.values)):

            key = response.fields[response_name].list_value.values[count].message_value.fields[
                entity_field_id].simple_value
            value = response.fields[response_name].list_value.values[count].message_value.fields[
                field_name].simple_value
            info.update({key: value})
        return info

    def get_case_id(self):
        return self.case_id

    def set_case_id(self, case_id):
        self.case_id = case_id

    def get_session_alias(self):
        return self.session_alias

    def set_session_alias(self, session_alias):
        self.session_alias = session_alias
