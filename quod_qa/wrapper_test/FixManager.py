from re import match

from th2_grpc_act_fix_quod.act_fix_pb2 import PlaceMessageRequest

from custom import basic_custom_actions
from quod_qa.wrapper_test.FixMessage import FixMessage
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from stubs import Stubs


class FixManager:

    def __init__(self, session_alias, case_id = None):
        self.simulator = Stubs.simulator
        self.act = Stubs.fix_act
        self.__session_alias = session_alias
        self.__case_id = case_id

    def send_message(self, fix_message: FixMessage) -> None:
        # TODO add validation(valid MsgType)
        self.act.sendMessage(
            request=basic_custom_actions.convert_to_request(
                "Send " + fix_message.get_message_type() + " to connectivity " + self.get_session_alias(),
                self.get_session_alias(),
                self.get_case_id(),
                basic_custom_actions.message_to_grpc(fix_message.get_message_type(), fix_message.get_parameters(), self.__session_alias)
            ))

    def send_message_and_receive_response(self, fix_message: FixMessage) -> PlaceMessageRequest:
        if fix_message.get_message_type() == "D":
            response = self.act.placeOrderFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send NewOrderSingle",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc('NewOrderSingle', fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == "G":
            response = self.act.placeOrderReplaceFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelReplaceRequest",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc('OrderCancelReplaceRequest', fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == "F":
            response = self.act.placeOrderCancelFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelRequest",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc('OrderCancelRequest', fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        else:
            response = None

        # TODO add check which act method user should use
        # TODO return not PlaceMessageRequest but FixMessage
        return response

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def get_session_alias(self):
        return self.__session_alias

    def set_session_alias(self, session_alias):
        self.__session_alias = session_alias
