import logging

from th2_grpc_act_fix_quod.act_fix_pb2 import PlaceMessageRequest

from custom import basic_custom_actions
from custom.verifier import Verifier, VerificationMethod
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from test_framework.fix_wrappers.FixMessageBusinessMessageRejectReport import FixMessageBusinessMessageRejectReport
from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageListStatus import FixMessageListStatus
from test_framework.fix_wrappers.FixMessageMarketDataIncrementalRefresh import FixMessageMarketDataIncrementalRefresh
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageMarketDataSnapshotFullRefresh import FixMessageMarketDataSnapshotFullRefresh
from stubs import Stubs
from test_framework.fix_wrappers.FixMessageOrderCancelRejectReport import FixMessageOrderCancelRejectReport
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestRejectFX import FixMessageMarketDataRequestRejectFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestRejectFX import FixMessageQuoteRequestRejectFX


class FixManager:

    def __init__(self, session_alias, case_id=None):
        self.simulator = Stubs.simulator
        self.act = Stubs.fix_act
        self.__session_alias = session_alias
        self.__case_id = case_id
        self.verifier = Verifier(self.__case_id)
        self.response = None

    def send_message(self, fix_message: FixMessage, custom_message=None) -> None:
        logging.info(f"Message {fix_message.get_message_type()} sent with params -> {fix_message.get_parameters()}")
        # TODO add validation(valid MsgType)
        if custom_message == None:
            message = "Send "
        else:
            message = custom_message
        self.act.sendMessage(
            request=basic_custom_actions.convert_to_request(
                message + fix_message.get_message_type() + " to connectivity " + self.get_session_alias(),
                self.get_session_alias(),
                self.get_case_id(),
                basic_custom_actions.message_to_grpc(fix_message.get_message_type(), fix_message.get_parameters(),
                                                     self.__session_alias)
            ))

    def send_quote_to_dealer_and_receive_response(self, fix_message: FixMessage, case_id=None):
        logging.info(f"Message {fix_message.get_message_type()} sent with params -> {fix_message.get_parameters()}")
        if case_id is not None:
            case_id = self.__case_id
        response = self.act.sendQuoteViaWindow(
            request=basic_custom_actions.convert_to_request(
                "Send QuoteRequest to Dealer Intervention",
                self.__session_alias,
                case_id,
                basic_custom_actions.message_to_grpc(FIXMessageType.QuoteRequest.value, fix_message.get_parameters(),
                                                     self.__session_alias)
            ))
        return response

    def send_message_and_receive_response(self, fix_message: FixMessage, case_id=None) -> list:
        logging.info(f"Message {fix_message.get_message_type()} sent with params -> {fix_message.get_parameters()}")
        if case_id == None:
            case_id = self.__case_id

        if fix_message.get_message_type() == FIXMessageType.NewOrderSingle.value:
            response = self.act.placeOrderFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send NewOrderSingle",
                    self.__session_alias,
                    case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.NewOrderSingle.value, fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelReplaceRequest.value:
            response = self.act.placeOrderReplaceFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelReplaceRequest",
                    self.__session_alias,
                    case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.OrderCancelReplaceRequest.value,
                                                         fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelRequest.value:
            response = self.act.placeOrderCancelFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelRequest",
                    self.__session_alias,
                    case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.OrderCancelRequest.value,
                                                         fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.MarketDataSnapshotFullRefresh.value:
            response = self.act.sendMessage(
                request=basic_custom_actions.convert_to_request(
                    "Send MarketDataSnapshotFullRefresh",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.MarketDataSnapshotFullRefresh.value,
                                                         fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.MarketDataIncrementalRefresh.value:
            response = self.act.sendMessage(
                request=basic_custom_actions.convert_to_request(
                    "Send MarketDataIncrementalRefresh",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.MarketDataIncrementalRefresh.value,
                                                         fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.MarketDataRequest.value:
            response = self.act.placeMarketDataRequestFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send MarketDataRequest",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.MarketDataRequest.value,
                                                         fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.QuoteRequest.value:
            response = self.act.placeQuoteFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send Request For Quote",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.QuoteRequest.value,
                                                         fix_message.get_parameters(),
                                                         self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.NewOrderMultiLeg.value:
            response = self.act.placeOrderMultilegFIX(
                request=basic_custom_actions.convert_to_request(
                    "Sen New Order Multi Leg",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc(FIXMessageType.NewOrderMultiLeg.value,
                                                         fix_message.get_parameters(),
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
                            fields.update({field: repeating_group_list})
            message_type = message.metadata.message_type
            response_fix_message = None
            if message_type == FIXMessageType.NewOrderSingle.value:
                response_fix_message = FixMessageNewOrderSingle()
            elif message_type == FIXMessageType.ExecutionReport.value:
                response_fix_message = FixMessageExecutionReport()
            elif message_type == FIXMessageType.MarketDataSnapshotFullRefresh.value:
                response_fix_message = FixMessageMarketDataSnapshotFullRefresh()
            elif message_type == FIXMessageType.MarketDataIncrementalRefresh.value:
                response_fix_message = FixMessageMarketDataIncrementalRefresh()
            elif message_type == FIXMessageType.Quote.value:
                response_fix_message = FixMessageQuoteFX()
            elif message_type == FIXMessageType.NewOrderMultiLeg.value:
                response_fix_message = FixMessageNewOrderMultiLegFX()
            elif message_type == FIXMessageType.MarketDataRequestReject.value:
                response_fix_message = FixMessageMarketDataRequestRejectFX()
            elif message_type == FIXMessageType.QuoteRequestReject.value:
                response_fix_message = FixMessageQuoteRequestRejectFX()
            elif message_type == FIXMessageType.OrderCancelReject.value:
                response_fix_message = FixMessageOrderCancelRejectReport()
            elif message_type == FIXMessageType.BusinessMessageReject.value:
                response_fix_message = FixMessageBusinessMessageRejectReport()
            response_fix_message.change_parameters(fields)

            response_messages.append(response_fix_message)

            for i in response_messages:
                logging.info(f"Received message is {i.get_message_type()} with params ->"
                             f" {i.get_parameters()}")
        self.response = response_messages
        return response_messages

    def send_message_fix_standard(self, fix_message: FixMessage) -> None:
        # TODO add validation(valid MsgType)
        self.act.sendMessage(
            request=basic_custom_actions.convert_to_request(
                "Send " + fix_message.get_message_type() + " to connectivity " + self.get_session_alias(),
                self.get_session_alias(),
                self.get_case_id(),
                basic_custom_actions.message_to_grpc_fix_standard(fix_message.get_message_type(),
                                                                  fix_message.get_parameters(), self.__session_alias)
            ))

    def send_message_and_receive_response_fix_standard(self, fix_message: FixMessage) -> PlaceMessageRequest:
        if fix_message.get_message_type() == FIXMessageType.NewOrderSingle.value:
            response = self.act.placeOrderFIXDelay(
                request=basic_custom_actions.convert_to_request(
                    "Send NewOrderSingle",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc_fix_standard(FIXMessageType.NewOrderSingle.value,
                                                                      fix_message.get_parameters(),
                                                                      self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelReplaceRequest.value:
            response = self.act.placeOrderReplaceFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelReplaceRequest",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc_fix_standard(FIXMessageType.OrderCancelReplaceRequest.value,
                                                                      fix_message.get_parameters(),
                                                                      self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.OrderCancelRequest.value:
            response = self.act.placeOrderCancelFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send OrderCancelRequest",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc_fix_standard(FIXMessageType.OrderCancelRequest.value,
                                                                      fix_message.get_parameters(),
                                                                      self.__session_alias)
                ))
        elif fix_message.get_message_type() == FIXMessageType.NewOrderList.value:
            response = self.act.placeOrderListFIX(
                request=basic_custom_actions.convert_to_request(
                    "Send NewOrderList",
                    self.__session_alias,
                    self.__case_id,
                    basic_custom_actions.message_to_grpc_fix_standard(FIXMessageType.NewOrderList.value,
                                                                      fix_message.get_parameters(),
                                                                      self.__session_alias)
                ))
        else:
            response = None

        return self.parse_response_fix_standard(response)

    def parse_response_fix_standard(self, response: PlaceMessageRequest) -> list:
        response_messages = list()
        for message in response.response_messages_list:
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

            if message_type == FIXMessageType.NewOrderSingle.value:
                response_fix_message = FixMessageNewOrderSingle()
            elif message_type == FIXMessageType.ExecutionReport.value:
                response_fix_message = FixMessageExecutionReport()
            elif message_type == FIXMessageType.ListStatus.value:
                response_fix_message = FixMessageListStatus()
            elif message_type == FIXMessageType.OrderCancelReplaceRequest.value:
                response_fix_message = FixMessageOrderCancelReplaceRequest()
            response_fix_message.change_parameters(fields)

            response_messages.append(response_fix_message)
        self.response = response_messages
        return response_messages

    def get_case_id(self):
        return self.__case_id

    def set_case_id(self, case_id):
        self.__case_id = case_id

    def get_session_alias(self):
        return self.__session_alias

    def set_session_alias(self, session_alias):
        self.__session_alias = session_alias

    def compare_values(self, expected_values: dict, actual_values: dict, event_name: str,
                       verification_method: VerificationMethod = VerificationMethod.EQUALS):
        self.verifier.set_event_name(event_name)
        try:
            for k, v in expected_values.items():
                self.verifier.compare_values("Compare: " + k, v, actual_values[k],
                                             verification_method)
        except KeyError:
            raise KeyError(f"Element: {k} not found")
        self.verifier.verify()
        self.verifier = Verifier(self.__case_id)

    def key_is_absent(self, key: str, actual_values: dict, event_name: str):
        if key in actual_values:
            self.verifier.success = False

        self.verifier.fields.update(
            {"Is absent:": {"expected": key, "key": False, "type": "field",
                            "status": "PASSED" if self.verifier.success else "FAILED"}})
        self.verifier.set_event_name(event_name)
        self.verifier.verify()
        self.verifier = Verifier(self.__case_id)

    def get_last_message(self, message_type, filter_value=None) -> FixMessage:
        self.response.reverse()
        for res in self.response:
            if res.get_message_type() == message_type:
                if filter_value and str(res.get_parameters()).find(filter_value) == -1:
                    continue
                self.response.reverse()
                return res
        raise KeyError(f"{message_type} not found")

    def get_first_message(self, message_type, filter_value=None) -> FixMessage:
        for res in self.response:
            if res.get_message_type() == message_type:
                if filter_value and str(res.get_parameters()).find(filter_value) == -1:
                    continue
                self.response.reverse()
                return res
        raise KeyError(f"{message_type} not found")