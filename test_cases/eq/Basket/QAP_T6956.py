import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    OrdListNotificationConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6956(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListFromExistingOrders()
        self.wave_creation_request = OrderListWaveCreationRequest()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.ord_sub1 = OrderSubmitOMS(self.data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value, external_algo_twap=True)
        self.ord_sub2 = OrderSubmitOMS(self.data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value, external_algo_twap=True)
        self.basket_name = 'QAP_T6956'
        self.urg = 'LOW'
        self.route = self.data_set.get_route_id_by_name('route_1')
        self.route = self.data_set.get_route("route_1")
        self.strategy = "MS TWAP(ASIA)"
        self.percentage_profile = "RemainingQty"
        self.str_tag = "TWAP"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create orders
        self.java_api_manager.send_message_and_receive_response(self.ord_sub1)
        order_id1 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        self.java_api_manager.send_message_and_receive_response(self.ord_sub2)
        order_id2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region create basket
        self.list_creation_request.set_default([order_id1, order_id2], self.basket_name)
        responses = self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        self.return_result(responses, ORSMessageType.NewOrderListReply.value)
        list_notify_block = self.result.get_parameter('NewOrderListReplyBlock')
        lis_id = list_notify_block['OrderListID']
        # endregion

        # region wave basket
        self.wave_creation_request.set_default(lis_id, [order_id1, order_id2])
        params = {"AlgoParametersBlock": {"AlgoType": "External",
                                          "ScenarioID": "102",
                                          "AlgoPolicyID": "1000132"},
                  "ExternalAlgoParametersBlock": {"ExternalAlgoParameterListBlock":
                      {"ExternalAlgoParameterBlock": [
                          {'AlgoParameterName': "Urgency",
                           "AlgoParamString": "MEDIUM",
                           'VenueScenarioParameterID': "7504"}]},
                      'ScenarioID': "102",
                      "ScenarioIdentifier": "11799",
                      "VenueScenarioID": "TWAP",
                      "VenueScenarioVersionID": "11945",
                      "VenueScenarioVersionValue": "ATDLEQ5.5"}, 'RouteID': 1}
        self.wave_creation_request.update_fields_in_component('OrderListWaveCreationRequestBlock', params)
        responses = self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        # endregion

        # region wave status
        self.return_result(responses, ORSMessageType.OrderListWaveNotification.value)
        list_notify_block = self.result.get_parameter('OrderListWaveNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_NEW.value},
            list_notify_block, 'Check Wave Status')
        # endregion

        # region check algo parameters in order
        self.return_result(responses, ORSMessageType.OrdReply.value)
        algo_param_block = self.result.get_parameter('OrdReplyBlock')['ExternalAlgoParametersBlock']
        self.java_api_manager.compare_values(
            {'ScenarioID': '102'},
            algo_param_block, 'Check child order algo')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
