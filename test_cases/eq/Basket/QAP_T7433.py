import random
import string
import logging
import time
from pathlib import Path
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.win_gui_wrappers.java_api_constants import SubmitRequestConst, OrdListNotificationConst, \
    JavaApiFields, ExecutionReportConst, ExecutionPolicyConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7433(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name('client_counterpart_1')
        self.basket_name = "Basket_" + "".join(random.choices(string.ascii_letters + string.digits, k=5))
        self.route_desk = "Route via FIXBUYTH2 - component used by TH2 simulator and autotests"
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.route = self.data_set.get_route('route_1')
        self.strategy = "TWAP"
        self.new_order_list = NewOrderListOMS(self.data_set).set_default_order_list()
        self.create_wave_request = OrderListWaveCreationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create basket
        self.__create_basket()
        # endregion
        # region Wave Basket
        self.create_wave_request.set_default(self.basket_id, [self.order_id1, self.order_id2])
        algo_params = {"AlgoParametersBlock": {"AlgoType": "External",
                                               "ScenarioID": "101",
                                               "AlgoPolicyID": "1000131"},
                       "ExternalAlgoParametersBlock": {"ExternalAlgoParameterListBlock":
                           {"ExternalAlgoParameterBlock": [
                               {'AlgoParameterName': "StrategyTag",
                                "AlgoParamString": "TWAP",
                                'VenueScenarioParameterID': "7505"}]},
                           'ScenarioID': "101",
                           "ScenarioIdentifier": "8031",
                           "VenueScenarioID": "TWAP",
                           "VenueScenarioVersionID": "9682",
                           "VenueScenarioVersionValue": "ATDLEQ5.3.1"}, "RouteID": self.route_id}
        self.create_wave_request.update_fields_in_component('OrderListWaveCreationRequestBlock', algo_params)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.java_api_manager.send_message_and_receive_response(self.create_wave_request)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region check wave
        list_wave_notif = self.java_api_manager.get_last_message(ORSMessageType.OrderListWaveNotification.value)
        wave_notif_block = list_wave_notif.get_parameter(JavaApiFields.OrderListWaveNotificationBlock.value)
        print(wave_notif_block)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_TER.value,
             JavaApiFields.PercentQtyToRelease.value: '1.0', JavaApiFields.RouteID.value: str(self.route_id)}, {
                JavaApiFields.OrderListWaveStatus.value:
                    wave_notif_block[
                        JavaApiFields.OrderListWaveStatus.value],
                JavaApiFields.PercentQtyToRelease.value:
                    wave_notif_block[
                        JavaApiFields.PercentQtyToRelease.value], JavaApiFields.RouteID.value: wave_notif_block[
                    JavaApiFields.RouteID.value]},
            "Check Wave values")
        # endregion
        # region child orders
        order_1_block = wave_notif_block[JavaApiFields.OrderNotificationElements.value][
            JavaApiFields.OrderNotificationBlock.value][0]
        order_2_block = wave_notif_block[JavaApiFields.OrderNotificationElements.value][
            JavaApiFields.OrderNotificationBlock.value][1]
        # endregion
        # region first child order
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value,
             JavaApiFields.ExternalAlgo.value: 'Y', JavaApiFields.RouteID.value: str(self.route_id)}, {
                JavaApiFields.TransExecStatus.value:
                    order_1_block[
                        JavaApiFields.TransExecStatus.value],
                JavaApiFields.ExecutionPolicy.value: order_1_block[JavaApiFields.ExecutionPolicy.value],
                JavaApiFields.ExternalAlgo.value:
                    order_1_block[JavaApiFields.ExternalAlgo.value],
                JavaApiFields.RouteID.value: order_1_block[
                    JavaApiFields.RouteID.value]},
            "Check first order fields")
        # endregion
        # region second child order
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value,
             JavaApiFields.ExternalAlgo.value: 'Y', JavaApiFields.RouteID.value: str(self.route_id)}, {
                JavaApiFields.TransExecStatus.value:
                    order_2_block[
                        JavaApiFields.TransExecStatus.value],
                JavaApiFields.ExecutionPolicy.value: order_1_block[JavaApiFields.ExecutionPolicy.value],
                JavaApiFields.ExternalAlgo.value:
                    order_2_block[JavaApiFields.ExternalAlgo.value],
                JavaApiFields.RouteID.value: order_2_block[
                    JavaApiFields.RouteID.value]},
            "Check second order fields")
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    def __create_basket(self):
        # create first order
        self.order_submit1 = OrderSubmitOMS(self.data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit1.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client})
        responses1 = self.java_api_manager.send_message_and_receive_response(self.order_submit1)
        self.__return_result(responses1, ORSMessageType.OrdReply.value)
        self.order_id1 = self.result.get_parameter('OrdReplyBlock')['OrdID']
        self.price = self.order_submit1.get_parameter('NewOrderSingleBlock')['Price']
        self.qty = self.order_submit1.get_parameter('NewOrderSingleBlock')['OrdQty']
        # endregion
        # create second order
        self.order_submit2 = OrderSubmitOMS(self.data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit2.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client})
        responses2 = self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        self.__return_result(responses2, ORSMessageType.OrdReply.value)
        self.order_id2 = self.result.get_parameter('OrdReplyBlock')['OrdID']
        # endregion
        # create basket
        new_params = {'NewOrderListBlock': {
            "OrdIDList": {"OrdIDBlock": [{"OrdID": self.order_id1}, {"OrdID": self.order_id2}]},
            "OrderListName": self.basket_name}}
        self.new_order_list.change_parameters(new_params)
        self.new_order_list.remove_parameter('CDOrdAssignInstructionsBlock')
        basket_responses = self.java_api_manager.send_message_and_receive_response(self.new_order_list)
        self.__return_result(basket_responses, ORSMessageType.OrdListNotification.value)
        self.basket_id = self.result.get_parameter('OrdListNotificationBlock')['OrderListID']
        # endregion
