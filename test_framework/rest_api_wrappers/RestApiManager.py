from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from custom.basic_custom_actions import convert_to_get_request
from stubs import Stubs
from custom import basic_custom_actions as bca
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
    def parse_response_details(response, filter_dict: dict = None):
        """
        This method used to parse received response from GET message
        (e.g. removing some unnecessary system keys and tags from raw response)
        and applying filter to result if needed
        """
        result = dict()
        result_list = []
        temp = dict()
        for i in MessageToDict(response)['fields']:                                                 #
            temp = MessageToDict(response)['fields'][i]['listValue']['values']                      # Parsing received results to a format:
        for i in range(len(temp)):                                                                  # {key:{item.key: item.value}}
            result.update({i: temp[i]['messageValue']['fields']})                                   #
        temp.clear()
        for i in result.keys():
            temp = result[i]
            for key, value in temp.items():                                                         # Deleting unnecessary keys from raw response.
                if 'simpleValue' in value.keys():                                                   # If value is simple adding it to result
                    temp.update({key: value['simpleValue']})                                        # else removing unnecessary keys from sub-list
                elif 'listValue' in value.keys():                                                   #
                    temp_list = []
                    for list_values in value['listValue']['values']:
                        temp_dict = dict()
                        for list_key, list_value in list_values['messageValue']['fields'].items():  #
                            if 'simpleValue' in list_value.keys():                                  # Some of sub-elements can be coplex too
                                temp_dict.update({list_key: list_value['simpleValue']})             # so starting removing of system keys from 2nd sub-list
                            elif 'listValue' in list_value.keys():                                  # of course further nesting is not excluded
                                sub_list=[]                                                         # but it very unlikley to face with them throughout system
                                for sub_list_values in list_value['listValue']['values']:           #
                                    sub_dict = dict()
                                    for sub_list_key, sub_list_value in sub_list_values['messageValue']['fields'].items():
                                        sub_dict.update({sub_list_key: sub_list_value['simpleValue']})
                                    sub_list.append(sub_dict)
                                temp_dict.update({list_key: sub_list})
                        temp_list.append(temp_dict)
                    temp.update({key: temp_list})
            result.update({i: temp})
        if filter_dict is not None:                                                                 #
            result_out_of_filter = dict()                                                           # If dict of filters is present, applying it to result
            filtered_result = dict()                                                                #
            for key, value in result.items():
                for filter_key, filter_value in filter_dict.items():
                    if str(value[filter_key]) != str(filter_value):
                        result_out_of_filter.update({key: value})
            for key in result.keys():
                if key not in result_out_of_filter.keys():
                    filtered_result.update({key: result[key]})
            for key in filtered_result.keys():
                result_list.append(filtered_result[key])
        else:
            for key in result.keys():
                result_list.append(result[key])
        return result_list

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
