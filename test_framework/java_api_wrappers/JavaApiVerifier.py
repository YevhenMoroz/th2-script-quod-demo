from th2_grpc_common.common_pb2 import Direction

from stubs import Stubs
import re
from copy import deepcopy
from typing import Union

from test_framework.data_sets.message_types import PKSMessageType, MPASMessageType
from test_framework.fix_wrappers.DataSet import DirectionEnum
from custom import basic_custom_actions
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class JavaApiVerifier:
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

    def check_java_message(self, java_message: JavaApiMessage, key_parameters: list = None,
                           direction: DirectionEnum = DirectionEnum.FromQuod, message_name: str = None,
                           ignored_fields: list = None):
        if java_message.get_message_type() == PKSMessageType.FixRequestForPositionsAck.value:
            if key_parameters is None:
                key_parameters = ["ClientPosReqID"]

            if message_name is None:
                message_name = "Check RequestForPositionsAck  message"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(f"{PKSMessageType.FixRequestForPositionsAck.value}",
                                                        java_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif java_message.get_message_type() == MPASMessageType.AutoHedgerInstrSymbolBatchUpdate.value:
            if key_parameters is None:
                key_parameters = ["AutoHedgerID"]

            if message_name is None:
                message_name = "Check AutoHedgerInstrSymbolBatchUpdateBlock  message"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(f"{MPASMessageType.AutoHedgerInstrSymbolBatchUpdate.value}",
                                                        java_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        elif java_message.get_message_type() == PKSMessageType.FixPositionReport.value:
            if key_parameters is None:
                key_parameters = ["ClientPosReqID"]

            if message_name is None:
                message_name = "Check PositionReport  message"
            self.__verifier.submitCheckRule(
                basic_custom_actions.create_check_rule(
                    message_name,
                    basic_custom_actions.filter_to_grpc(f"{PKSMessageType.FixPositionReport.value}",
                                                        java_message.get_parameters(),
                                                        key_parameters, ignored_fields),
                    self.__checkpoint,
                    self.__session_alias,
                    self.__case_id,
                    Direction.Value(direction.value)
                )
            )
        else:
            pass
# TODO add exeption into els
