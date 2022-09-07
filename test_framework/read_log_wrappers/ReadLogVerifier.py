from th2_grpc_common.common_pb2 import Direction

from custom import basic_custom_actions
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import DirectionEnum


class ReadLogVerifier:
    def __init__(self, session_alias, case_id=None):
        self.__verifier = Stubs.verifier
        self.__session_alias = session_alias
        self.__case_id = case_id
        self.__checkpoint = self.__verifier.createCheckpoint(
            basic_custom_actions.create_checkpoint_request(self.__case_id)).checkpoint

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def check_read_log_message(self, compare_message: dict, key_parameters: list = None,
                               direction: DirectionEnum = DirectionEnum.FromQuod, timeout: int = 3000):
        self.__verifier.submitCheckRule(
            basic_custom_actions.create_check_rule(
                "Log Msg Received",
                basic_custom_actions.filter_to_grpc_fix_standard("Csv_Message", compare_message, key_parameters),
                self.__checkpoint,
                self.__session_alias,
                self.__case_id,
                Direction.Value(direction.value),
                timeout
            )
        )

    def check_read_log_message_sequence(self, compare_messages_list: list, key_parameters_list: list = None, direction: DirectionEnum = DirectionEnum.FromQuod,
                                   message_name: str = None, pre_filter: dict = None):
        if pre_filter is not None:
            pre_filter_req = basic_custom_actions.prefilter_to_grpc(pre_filter)
        else:
            pre_filter_req = None
        message_filters_req = list()
        if len(compare_messages_list) != len(key_parameters_list):
            raise ValueError("Not correct qty of object at list expect len(fix_messages_list) equal len(key_parameters_list)")

        for index, message in enumerate(compare_messages_list):
            message_filters_req.append(basic_custom_actions.filter_to_grpc("Csv_Message", message, key_parameters_list[index]))

        if message_name is None:
            message_name = "Check banch of messages"

        self.__verifier.submitCheckSequenceRule(
            basic_custom_actions.create_check_sequence_rule(
                description=message_name,
                prefilter=pre_filter_req,
                msg_filters=message_filters_req,
                checkpoint=self.__checkpoint,
                connectivity=self.__session_alias,
                event_id=self.__case_id,
                direction=Direction.Value(direction.value)
            )
        )