import re
from copy import deepcopy

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
                          direction: DirectionEnum = DirectionEnum.FromQuod, message_name: str = None,
                          ignored_fields: list = None):
        if fix_message.is_parameter_exist('TransactTime') and fix_message.get_parameter('TransactTime')[0] not in (
        '!', '%', '<', '>', '%'):
            fix_message = deepcopy(fix_message)
            fix_message.change_parameter('TransactTime', "*")
        if fix_message.get_message_type() == FIXMessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            if message_name is None:
                message_name = "Check NewOrderSingle"

            if fix_message.is_parameter_exist('TransactTime') and fix_message.get_parameter('TransactTime')[0] not in (
            '!', '%', '<', '>', '%'):
                fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
                if re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:00').search(fix_message.get_parameter('TransactTime')):
                    fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime')[:-3])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(FIXMessageType.NewOrderSingle.value,
                                                        fix_message.get_parameters(),
                                                        key_parameters,
                                                        ignored_fields),
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
                                                        key_parameters,
                                                        ignored_fields),
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
                                                        key_parameters, ignored_fields),
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
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.MarketDataSnapshotFullRefresh.value:
            if key_parameters is None:
                key_parameters = ['MDReqID']

            if message_name is None:
                message_name = "Check MarketDataSnapshotFullRefresh"

            # fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("MarketDataSnapshotFullRefresh", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.MarketDataIncrementalRefresh.value:
            if key_parameters is None:
                key_parameters = ['MDReqID']

            if message_name is None:
                message_name = "Check MarketDataIncrementalRefresh"

            # fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("MarketDataIncrementalRefresh", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelReject.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID']
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check OrderCancelReject",
                    basic_custom_actions.filter_to_grpc(FIXMessageType.OrderCancelReject.value,
                                                        fix_message.get_parameters(), key_parameters, ignored_fields),
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
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.MarketDataRequestReject.value:
            if key_parameters is None:
                key_parameters = ["MDReqID"]

            if message_name is None:
                message_name = "Check Market Data Reject"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("MarketDataRequestReject", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.QuoteRequestReject.value:
            if key_parameters is None:
                key_parameters = ["QuoteReqID"]

            if message_name is None:
                message_name = "Check QuoteRequest Reject"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("QuoteRequestReject", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.QuoteCancel.value:
            if key_parameters is None:
                key_parameters = ["QuoteReqID"]

            if message_name is None:
                message_name = "Check QuoteCancel message"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("QuoteCancel", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.BusinessMessageReject.value:
            if key_parameters is None:
                key_parameters = ['RefMsgType']

            if message_name is None:
                message_name = "Check BusinessMessageReject"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("BusinessMessageReject", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.QuoteRequest.value:
            if key_parameters is None:
                key_parameters = ["QuoteReqID"]

            if message_name is None:
                message_name = "Check QuoteRequest message"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("QuoteRequest", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.AllocationACK.value:
            if key_parameters is None:
                key_parameters = ["AllocID", "AllocStatus"]
            if message_name is None:
                message_name = "Check AllocationACK message"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc("AllocationACK", fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        else:
            pass
        # TODO add exeption into else

    def check_fix_message_sequence(self, fix_messages_list: list, key_parameters_list: list = None,
                                   direction: DirectionEnum = DirectionEnum.FromQuod,
                                   message_name: str = None, pre_filter: dict = None, check_order=True):
        if pre_filter is None:
            pre_filter = {
                'header': {
                    'MsgType': ('0', "NOT_EQUAL")
                }
            }

        pre_filter_req = basic_custom_actions.prefilter_to_grpc(pre_filter)
        message_filters_req = list()
        if len(fix_messages_list) != len(key_parameters_list):
            raise ValueError(
                "Not correct qty of object at list expect len(fix_messages_list) equal len(key_parameters_list)")

        for index, message in enumerate(fix_messages_list):
            if not isinstance(message, FixMessage):
                raise ValueError("Not correct object type at fix_messages_list, expect only FixMessages")
            message_filters_req.append(
                basic_custom_actions.filter_to_grpc(message.get_message_type(), message.get_parameters(),
                                                    key_parameters_list[index]))

        if message_name is None:
            message_name = "Check banch of messages"

        self.__verifier.submitCheckSequenceRule(
            basic_custom_actions.create_check_sequence_rule(
                check_order=check_order,
                description=message_name,
                prefilter=pre_filter_req,
                msg_filters=message_filters_req,
                checkpoint=self.__checkpoint,
                connectivity=self.__session_alias,
                event_id=self.__case_id,
                direction=Direction.Value(direction.value)
            )
        )

    def check_no_message_found(self, message_timeout: 10000, direction: DirectionEnum = DirectionEnum.FromQuod, message_name: str = None, pre_filter: dict = None):
        if pre_filter is None:
            pre_filter = {
                'header': {
                    'MsgType': ('0', "NOT_EQUAL")
                }
            }
        pre_filter_req = basic_custom_actions.prefilter_to_grpc(pre_filter)

        if message_name is None:
            message_name = "Check no message found"

        self.__verifier.submitNoMessageCheck (
            basic_custom_actions.create_check_no_message_found(
                description=message_name,
                prefilter=pre_filter_req,
                message_timeout=message_timeout,
                checkpoint=self.__checkpoint,
                connectivity=self.__session_alias,
                event_id=self.__case_id,
                timeout=20000,
                direction=Direction.Value(direction.value)
            )
        )


    def check_fix_message_fix_standard(self, fix_message: FixMessage, key_parameters: list = None,
                                       direction: DirectionEnum = DirectionEnum.FromQuod, ignored_fields: list = None):
        if fix_message.get_message_type() == FIXMessageType.NewOrderSingle.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']
            fix_message.change_parameter('TransactTime', fix_message.get_parameter('TransactTime').split('.')[0])
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check NewOrderSingle",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.NewOrderSingle.value,
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
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
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
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
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
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
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
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
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelReject.value:
            if key_parameters is None:
                key_parameters = ['ClOrdID', 'OrdStatus']

            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check OrderCancelReject",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.OrderCancelReject.value,
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
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
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelReplaceRequest.value:
            if key_parameters is None:
                key_parameters = ['OrigClOrdID']
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    'Check OrderCancelReplaceRequest',
                    basic_custom_actions.filter_to_grpc(FIXMessageType.OrderCancelReplaceRequest.value,
                                                        fix_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif fix_message.get_message_type() == FIXMessageType.DontKnowTrade.value:
            if key_parameters is None:
                key_parameters = ['ExecID']
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    "Check DontKnowTrade",
                    basic_custom_actions.filter_to_grpc_fix_standard(FIXMessageType.DontKnowTrade.value,
                                                                     fix_message.get_parameters(), key_parameters,
                                                                     ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        else:
            pass
        # TODO add exeption into else
