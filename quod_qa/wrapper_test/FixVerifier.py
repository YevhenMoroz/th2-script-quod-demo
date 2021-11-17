
from custom import basic_custom_actions
from th2_grpc_common.common_pb2 import Direction

from quod_qa.wrapper_test.DataSet import MessageType, DirectionEnum
from quod_qa.wrapper_test.FixMessage import FixMessage
from stubs import Stubs


class FixVerifier:
    def __init__(self, session_alias, case_id=None):
        self.__verifier = Stubs.verifier
        self.__session_alias = session_alias
        self.__case_id = case_id
        self.__checkpoint = self.__verifier.createCheckpoint(basic_custom_actions.create_checkpoint_request(self.__case_id)).checkpoint

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def check_fix_message(self, fix_message: FixMessage, key_parameters: list = None, direction: DirectionEnum = DirectionEnum.FIRST):
        if fix_message.get_message_type() == MessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']
            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check NewOrderSingle",
                    basic_custom_actions.filter_to_grpc(MessageType.NewOrderSingle.value, fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == MessageType.ExecutionReport.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check ExecutionReport",
                    basic_custom_actions.filter_to_grpc(MessageType.ExecutionReport.value, fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        else:
            pass
        # TODO add exeption into else

    def check_fix_message_fix_standard(self, fix_message: FixMessage, key_parameters: list = None, direction: DirectionEnum = DirectionEnum.FIRST):
        if fix_message.get_message_type() == MessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']
            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check NewOrderSingle",
                    basic_custom_actions.filter_to_grpc_fix_standard(MessageType.NewOrderSingle.value, fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == MessageType.ExecutionReport.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check ExecutionReport",
                    basic_custom_actions.filter_to_grpc_fix_standard(MessageType.ExecutionReport.value, fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        else:
            pass
        # TODO add exeption into else


