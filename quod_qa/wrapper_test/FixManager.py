from th2_grpc_act_fix_quod.act_fix_pb2 import PlaceMessageRequest

from custom import basic_custom_actions
from quod_qa.wrapper_test.DataSet import MessageType
from quod_qa.wrapper_test.FixMessage import FixMessage
from quod_qa.wrapper_test.FixMessageExecutionReport import FixMessageExecutionReport
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from stubs import Stubs


class FixManager:

    def __init__(self, session_alias, case_id=None):
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

    def send_message_and_receive_response(self, fix_message: FixMessage, case= None) -> PlaceMessageRequest:
        if case == None:
            case = self.__case_id

        if fix_message.get_message_type() == MessageType.NewOrderSingle.value:
            response = self.act.placeOrderFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send NewOrderSingle",
                    self.__session_alias,
                    case,
                    basic_custom_actions.message_to_grpc(MessageType.NewOrderSingle.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == MessageType.OrderCancelReplaceRequest.value:
            response = self.act.placeOrderReplaceFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelReplaceRequest",
                    self.__session_alias,
                    case,
                    basic_custom_actions.message_to_grpc(MessageType.OrderCancelReplaceRequest.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == MessageType.OrderCancelRequest.value:
            response = self.act.placeOrderCancelFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelRequest",
                    self.__session_alias,
                    case,
                    basic_custom_actions.message_to_grpc(MessageType.OrderCancelRequest.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == MessageType.MarketDataSnapshotFullRefresh.value:
            response = self.act.sendMessage(
                request=basic_custom_actions.convert_to_request(
                    "Send MarketDataSnapshotFullRefresh",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(MessageType.MarketDataSnapshotFullRefresh.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == MessageType.MarketDataIncrementalRefresh.value:
            response = self.act.sendMessage(
                request=basic_custom_actions.convert_to_request(
                    "Send MarketDataIncrementalRefresh",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(MessageType.MarketDataIncrementalRefresh.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == MessageType.MarketDataRequest.value:
            response = self.act.placeMarketDataRequestFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send MarketDataRequest",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(MessageType.MarketDataRequest.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        else:
            response = None

        return self.parse_response(response)

    def parse_response(self, response: PlaceMessageRequest) -> list:
        response_messages = list()
        for message in response.response_messages_list:
            fields = dict()
            for field in message.fields:
                #Field
                if message.fields[field].simple_value != "":
                    fields.update({field: message.fields[field].simple_value})
                else:
                    component_fields = dict()
                    # Component
                    for component_field in message.fields[field].message_value.fields:
                        if message.fields[field].message_value.fields[component_field].simple_value != "":
                            component_fields.update({component_field: message.fields[field].message_value.fields[component_field].simple_value})
                            fields.update({field: component_fields})
                        else:
                            # Repeating Group
                            repeating_group_list = list()
                            for repeating_group in message.fields[field].message_value.fields[component_field].list_value.values:
                                repeating_group_list_field = dict()
                                for repeating_group_field in repeating_group.message_value.fields:
                                    repeating_group_list_field.update({repeating_group_field: repeating_group.message_value.fields[repeating_group_field].simple_value})
                                repeating_group_list.append(repeating_group_list_field)
                            fields.update({field: repeating_group_list})
            message_type = message.metadata.message_type
            responce_fix_message = None
            if message_type == MessageType.NewOrderSingle.value:
                responce_fix_message = FixMessageNewOrderSingle()
            elif message_type == MessageType.ExecutionReport.value:
                responce_fix_message = FixMessageExecutionReport()

            responce_fix_message.change_parameters(fields)

        response_messages.append(responce_fix_message)
        return response_messages

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def get_session_alias(self):
        return self.__session_alias

    def set_session_alias(self, session_alias):
        self.__session_alias = session_alias
