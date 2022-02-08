from custom import basic_custom_actions
from th2_grpc_common.common_pb2 import Direction

from test_framework.fix_wrappers.DataSet import DirectionEnum
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from stubs import Stubs


class FixVerifier:
    def __init__(self, session_alias, case_id=None, checkpoint=None):
        self.__verifier = Stubs.verifier
        self.__session_alias = session_alias
        self.__case_id = case_id
        if checkpoint is not None:
            self.__checkpoint = checkpoint
        else:
            self.__checkpoint = self.__verifier.createCheckpoint(
                basic_custom_actions.create_checkpoint_request(self.__case_id)).checkpoint

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def check_fix_message(self, fix_message: FixMessage, key_parameters: list = None,
                          direction: DirectionEnum = DirectionEnum.FromQuod, message_name: str = None):
        if fix_message.get_message_type() == FIXMessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check NewOrderSingle"

            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(FIXMessageType.NewOrderSingle.value,
                                                        fix_message.get_parameters(),
                                                        key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.ExecutionReport.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check ExecutionReport"

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(FIXMessageType.ExecutionReport.value,
                                                        fix_message.get_parameters(),
                                                        key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelReplaceRequest.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check OrderCancelReplaceRequest"

            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("OrderCancelReplaceRequest", fix_message.get_parameters(),
                                                        key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelRequest.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check OrderCancelRequest"

            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("OrderCancelRequest", fix_message.get_parameters(),
                                                        key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.MarketDataSnapshotFullRefresh.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check MarketDataSnapshotFullRefresh"

            # fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("MarketDataSnapshotFullRefresh", fix_message.get_parameters(),
                                                        key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.Quote.value:
            if key_parameters is None:
                key_parameters = ['QuoteReqID']

            if message_name is None:
                message_name = "Check Quote"

            # fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("Quote", fix_message.get_parameters(),
                                                        key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )

        else:
            pass
        # TODO add exeption into else

    def check_fix_message_fix_standard(self, fix_message: FixMessage, key_parameters: list = None,
                                       direction: DirectionEnum = DirectionEnum.FromQuod):
        if fix_message.get_message_type() == FIXMessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']
            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check NewOrderSingle",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.NewOrderSingle.value,
                                                                     fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.ExecutionReport.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus', 'ExecType']
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check ExecutionReport",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.ExecutionReport.value,
                                                                     fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.NewOrderList.value:
            if key_parameters is None:
                key_parameters = ['ListID']

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check ListStatus",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.NewOrderList.value,
                                                                     fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.ListStatus.value:
            if key_parameters is None:
                key_parameters = ['ListID', 'ListOrderStatus']

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check ListStatus",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.ListStatus.value,
                                                                     fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.Confirmation.value:
            if key_parameters is None:
                key_parameters = ['ConfirmTransType', 'NoOrders']

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check Confirmation",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.Confirmation.value,
                                                                     fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.AllocationInstruction.value:
            if key_parameters is None:
                key_parameters = ['AllocType', 'NoOrders']

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check AllocationInstruction",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.AllocationInstruction.value,
                                                                     fix_message.get_parameters(), key_parameters),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        else:
            pass
        # TODO add exeption into else
