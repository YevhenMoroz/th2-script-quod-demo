import logging

from google.protobuf.json_format import MessageToDict
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from test_framework.rest_api_wrappers.web_admin_api.WebAdminRestApiMessages import WebAdminRestApiMessages
from test_framework.rest_api_wrappers.utils.verifier import data_validation
from custom.basic_custom_actions import convert_to_get_request
from stubs import Stubs
from custom import basic_custom_actions as bca


class WebAdminRestApiManager:

    def __init__(self, session_alias, case_id=None):
        self.act = Stubs.api_service
        self.session_alias = session_alias
        self.case_id = case_id

    def send_post_request(self, api_message: WebAdminRestApiMessages):
        self.act.sendMessage(request=SubmitMessageRequest(message=bca.wrap_message(content=api_message.get_parameters(),
                                                                                   message_type=api_message.get_message_type(),
                                                                                   session_alias=self.session_alias),
                                                          parent_event_id=self.case_id))

    def send_get_request(self, api_message: WebAdminRestApiMessages):
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

    def send_get_request_with_parameters(self, api_message: WebAdminRestApiMessages):
        message = convert_to_get_request(description="Send Get request with parameters",
                                         connectivity=self.session_alias,
                                         event_id=self.case_id,
                                         message=bca.wrap_message(content=api_message.get_parameters(),
                                                                  message_type=api_message.get_message_type(),
                                                                  session_alias=self.session_alias),
                                         request_type=api_message.get_message_type(),
                                         response_type=api_message.get_message_type() + "Reply")
        response = self.act.sendGetRequest(message)

        return response.response_message

    def send_multiple_request(self, api_message: WebAdminRestApiMessages):
        message = convert_to_get_request(description="Send http requests: Post/Get",
                                         connectivity=self.session_alias,
                                         event_id=self.case_id,
                                         message=bca.wrap_message(content=api_message.get_parameters(),
                                                                  message_type=api_message.get_message_type(),
                                                                  session_alias=self.session_alias),
                                         request_type=api_message.get_message_type(),
                                         response_type=api_message.get_message_type() + "Reply")
        response = self.act.sendGetRequest(message)

        return response.response_message

    @staticmethod
    def parse_response_details(response, filter_dict: dict = None):
        """
        This method used to parse received response from GET message
        (e.g. removing some unnecessary system keys and tags from raw response)
        and applying filter to result if needed
        """
        try:
            result = dict()
            result_list = []
            temp = dict()
            for i in MessageToDict(response)['fields']:  #
                temp = MessageToDict(response)['fields'][i]['listValue'][
                    'values']  # Parsing received results to a format:
            for i in range(len(temp)):  # {key:{item.key: item.value}}
                result.update({i: temp[i]['messageValue']['fields']})  #
            temp.clear()
            for i in result.keys():
                temp = result[i]
                for key, value in temp.items():  # Deleting unnecessary keys from raw response.
                    if 'simpleValue' in value.keys():  # If value is simple adding it to result
                        temp.update({key: value['simpleValue']})  # else removing unnecessary keys from sub-list
                    elif 'listValue' in value.keys():  #
                        temp_list = []
                        for list_values in value['listValue']['values']:
                            temp_dict = dict()
                            for list_key, list_value in list_values['messageValue']['fields'].items():  #
                                if 'simpleValue' in list_value.keys():  # Some of sub-elements can be coplex too
                                    temp_dict.update({list_key: list_value[
                                        'simpleValue']})  # so starting removing of system keys from 2nd sub-list
                                elif 'listValue' in list_value.keys():  # of course further nesting is not excluded
                                    sub_list = []  # but it very unlikley to face with them throughout system
                                    for sub_list_values in list_value['listValue']['values']:  #
                                        sub_dict = dict()
                                        for sub_list_key, sub_list_value in sub_list_values['messageValue'][
                                            'fields'].items():
                                            sub_dict.update({sub_list_key: sub_list_value['simpleValue']})
                                        sub_list.append(sub_dict)
                                    temp_dict.update({list_key: sub_list})
                            temp_list.append(temp_dict)
                        temp.update({key: temp_list})
                result.update({i: temp})
            if filter_dict is not None:  #
                result_out_of_filter = dict()  # If dict of filters is present, applying it to result
                filtered_result = dict()  #
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
        except Exception:
            logging.error("Error parsing", exc_info=True)

    @staticmethod
    def parse_response_error_message_details(response):
        try:
            response_to_dict = MessageToDict(response)  # Convert grpc message to dictionary
            if 'fields' in response_to_dict.keys():
                for key, _ in response_to_dict['fields'].items():
                    if key == 'errorMessage':
                        return response_to_dict['fields']['errorMessage']['simpleValue']
        except Exception:
            logging.error("Error parsing", exc_info=True)

    def risk_limit_dimension_verifier(self, test_id, response, rules_name, rule_parameters, step):

        verification_event = bca.create_event(f"Verification Step {step}", test_id)
        try:
            rule = self.parse_response_details(response, filter_dict={"riskLimitDimensionName": rules_name})
            for key, value in rule[0].items():
                if key != "alive" and key != "riskLimitDimensionID" and key != "institutionID":
                    if isinstance(rule[0][key], list):
                        for key_sub_list, value_sub_list in rule[0][key][0].items():
                            data_validation(test_id=verification_event,
                                            event_name=f"Step {step}. Check that value={value_sub_list} was set for {key_sub_list}",
                                            expected_result=str(rule_parameters[key][0][key_sub_list]),
                                            actual_result=rule[0][key][0][key_sub_list])
                    else:
                        data_validation(test_id=verification_event,
                                        event_name=f"Step {step}. Check that value={value} was set for {key}",
                                        expected_result=str(rule_parameters[key]),
                                        actual_result=rule[0][key])
        except (KeyError, TypeError, IndexError):
            bca.create_event(f'Step {step}. Response is empty.', status='FAILED', parent_id=verification_event)

    def get_response_details(self, response, response_name, expected_entity_name, entity_field_id):
        """
        Parameters:
            response: It is the object which we gets from "send_get_request" call
            response_name: This name we can find into dictionary(codec-json-wa) when describes message
            expected_entity_name: The name of the user for which you want to get information:
             For example(expected_entity_name: adm_rest), we gets data this user
            entity_field_id: It is name of field.
             For example: We want to get data about adm_rest user. The user adm_rest is the value of the field - userID
             So this value we set on this parameter
        """
        for count in range(len(response.fields[response_name].list_value.values)):
            entity = response.fields[response_name].list_value.values[count].message_value.fields[
                entity_field_id].simple_value
            if entity == expected_entity_name:
                return response.fields[response_name].list_value.values[count].message_value.fields

    @staticmethod
    def get_response_multiple_details(response, response_name, entity_field_id, field_name):

        info = {}
        for count in range(len(response.fields[response_name].list_value.values)):

            key = response.fields[response_name].list_value.values[count].message_value.fields[
                entity_field_id].simple_value
            try:
                desk_value = response.fields[response_name].list_value.values[count].message_value.fields[
                    field_name].list_value.values[0].message_value.fields['deskID'].simple_value
                print(desk_value)
                info.update({key: desk_value})
                # value = response.fields[response_name].list_value.values[count].message_value.fields[
                #     field_name].simple_value
            except:
                info.update({key: "User not assigned to some desk"})

        return info

    @staticmethod
    def get_user_hierarchy_level(response, response_name, user_id_field, hierarchy_level_id):

        info = {}
        for count in range(len(response.fields[response_name].list_value.values)):
            key = response.fields[response_name].list_value.values[count].message_value.fields[
                user_id_field].simple_value

            if hierarchy_level_id == 'institutionID':

                institution_value = response.fields[response_name].list_value.values[count].message_value.fields[
                    hierarchy_level_id].simple_value
                info.update({key: institution_value})
                if institution_value == '':
                    info.update({key: 'User not assigned to some institution'})

            if hierarchy_level_id == 'zoneID':

                zone_value = response.fields[response_name].list_value.values[count].message_value.fields[
                    hierarchy_level_id].simple_value
                info.update({key: zone_value})
                if zone_value == '':
                    info.update({key: 'User not assigned to some zone'})

            if hierarchy_level_id == 'locationID':

                location_value = response.fields[response_name].list_value.values[count].message_value.fields[
                    hierarchy_level_id].simple_value

                info.update({key: location_value})
                if location_value == '':
                    info.update({key: f'User {key} not assigned to some location'})

            try:
                if hierarchy_level_id == 'deskID':
                    desk_value = response.fields[response_name].list_value.values[count].message_value.fields[
                        'deskUserRole'].list_value.values[0].message_value.fields[hierarchy_level_id].simple_value
                    info.update({key: desk_value})
            except:
                info.update({key: f'User {key} not assigned to some desk'})

        return info

    def get_case_id(self):
        return self.case_id

    def set_case_id(self, case_id):
        self.case_id = case_id

    def get_session_alias(self):
        return self.session_alias

    def set_session_alias(self, session_alias):
        self.session_alias = session_alias
