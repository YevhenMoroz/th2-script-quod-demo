
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

    def check_fix_message(self, fix_message: FixMessage, key_parameters: list = None, direction: DirectionEnum = DirectionEnum.FromQuod, message_name: str = None):
        if fix_message.get_message_type() == MessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check NewOrderSingle"

            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(MessageType.NewOrderSingle.value, fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction)
                )
            )
        elif fix_message.get_message_type() == MessageType.ExecutionReport.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check ExecutionReport"

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(MessageType.ExecutionReport.value, fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction)
                )
            )
        elif fix_message.get_message_type() == MessageType.OrderCancelReplaceRequest.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check OrderCancelReplaceRequest"

            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("OrderCancelReplaceRequest", fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction)
                )
            )
        elif fix_message.get_message_type() == MessageType.OrderCancelRequest.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check OrderCancelRequest"

            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("OrderCancelRequest", fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction)
                )
            )
        else:
            pass
        # TODO add exeption into else




