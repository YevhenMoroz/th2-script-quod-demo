from th2_grpc_act_java_api_quod.act_java_api_quod_pb2 import ActJavaSubmitMessageRequest, ActJavaSubmitMessageResponses
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from test_framework.java_api_wrappers.ors_messages.ExecutionReport import ExecutionReport
from test_framework.java_api_wrappers.ors_messages.OrdNotification import OrdNotification
from test_framework.java_api_wrappers.ors_messages.OrdReply import OrdReply


class JavaApiManager:
    def __init__(self, session_alias, case_id=None):
        self.act = Stubs.act_java_api
        self.__session_alias = session_alias
        self.__case_id = case_id

    def send_message(self, message: JavaApiMessage) -> None:
        self.act.sendMessage(
            request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                         message.get_parameters(), self.get_session_alias()),
                parent_event_id=self.get_case_id()))

    def send_message_and_receive_response(self, message: JavaApiMessage):
        response = self.act.submitFixNewOrderSingle(
            request=ActJavaSubmitMessageRequest(
                message=bca.message_to_grpc_fix_standard(message.get_message_type(),
                                                         message.get_parameters(), self.get_session_alias()),
                parent_event_id=self.get_case_id()))
        return self.parse_response(response)

    def parse_response(self, response: ActJavaSubmitMessageResponses) -> list:
        response_messages = list()
        for message in response.response_message:
            fields = dict()
            for field in message.fields:
                # Field
                if message.fields[field].simple_value != "":
                    fields.update({field: message.fields[field].simple_value})
                else:
                    component_fields = dict()
                    # Component
                    for component_field in message.fields[field].message_value.fields:
                        if message.fields[field].message_value.fields[component_field].simple_value != "":
                            component_fields.update({component_field: message.fields[field].message_value.fields[
                                component_field].simple_value})
                            fields.update({field: component_fields})
                        else:
                            # Repeating Group
                            repeating_group_list = list()
                            for repeating_group in message.fields[field].message_value.fields[
                                component_field].list_value.values:
                                repeating_group_list_field = dict()
                                for repeating_group_field in repeating_group.message_value.fields:
                                    repeating_group_list_field.update({repeating_group_field:
                                                                           repeating_group.message_value.fields[
                                                                               repeating_group_field].simple_value})
                                repeating_group_list.append(repeating_group_list_field)
                            fields.update({field: {component_field: repeating_group_list}})
            message_type = message.metadata.message_type
            response_fix_message = None
            if message_type == ORSMessageType.OrdReply.value:
                response_fix_message = ExecutionReport()
            elif message_type == ORSMessageType.OrdNotification.value:
                response_fix_message = OrdNotification()
            elif message_type == ORSMessageType.ExecutionReport.value:
                response_fix_message = OrdReply()
            response_fix_message.change_parameters(fields)
            response_messages.append(response_fix_message)
        return response_messages

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def get_session_alias(self):
        return self.__session_alias

    def set_session_alias(self, session_alias):
        self.__session_alias = session_alias
