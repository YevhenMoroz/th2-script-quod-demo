import logging

from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdListNotificationConst, BasketMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveModificationRequest import \
    OrderListWaveModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7426(TestCase):

    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.create_wave_request = OrderListWaveCreationRequest()
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.list_wave_modify_request = OrderListWaveModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create basket
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        order_list_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameters()[
                JavaApiFields.OrdListNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            order_list_notification,
            'Check created first basket')
        list_id = order_list_notification['OrderListID']
        ord_id_1 = order_list_notification['OrdNotificationElements']['OrdNotificationBlock'][0][
            'OrdID']
        ord_id_2 = order_list_notification['OrdNotificationElements']['OrdNotificationBlock'][1][
            'OrdID']
        # endregion

        # region Wave Basket
        self.create_wave_request.set_default(list_id, [ord_id_1, ord_id_2])
        algo_params = {"AlgoParametersBlock": {"AlgoType": "External",
                                               "ScenarioID": "101",
                                               "AlgoPolicyID": "1000131"},
                       "ExternalAlgoParametersBlock": {"ExternalAlgoParameterListBlock":
                           {"ExternalAlgoParameterBlock": [
                               {'AlgoParameterName': "Urgency",
                                "AlgoParamString": "MEDIUM",
                                'VenueScenarioParameterID': "7504"}]},
                           'ScenarioID': "101",
                           "ScenarioIdentifier": "11799",
                           "VenueScenarioID": "TWAP",
                           "VenueScenarioVersionID": "11945",
                           "VenueScenarioVersionValue": "ATDLEQ5.5"}}
        self.create_wave_request.update_fields_in_component('OrderListWaveCreationRequestBlock', algo_params)
        self.java_api_manager.send_message_and_receive_response(self.create_wave_request)
        # endregion

        # region check wave
        list_wave_notif = self.java_api_manager.get_last_message(ORSMessageType.OrderListWaveNotification.value)
        wave_notif_block = list_wave_notif.get_parameter(JavaApiFields.OrderListWaveNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_NEW.value},
            wave_notif_block,
            "Check Wave sts values")
        self.java_api_manager.compare_values(
            {'ScenarioID': '101'},
            wave_notif_block['ExternalAlgoParametersBlock'],
            "Check Waves External Algo values")
        wave_id = wave_notif_block['OrderListWaveID']
        # endregion

        # region modifying wave
        self.list_wave_modify_request.set_default(wave_id, [ord_id_1, ord_id_2], list_id)
        algo_params = {"AlgoParametersBlock": {"AlgoType": "External",
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
                           "VenueScenarioVersionValue": "ATDLEQ5.5"}}
        self.list_wave_modify_request.update_fields_in_component('OrderListWaveModificationRequestBlock', algo_params)
        self.java_api_manager.send_message_and_receive_response(self.list_wave_modify_request)
        list_wave_notif = self.java_api_manager.get_last_message(ORSMessageType.OrderListWaveNotification.value)
        wave_notif_block = list_wave_notif.get_parameter(JavaApiFields.OrderListWaveNotificationBlock.value)
        self.java_api_manager.compare_values(
            {'ScenarioID': '102'},
            wave_notif_block['ExternalAlgoParametersBlock'],
            "Check Waves modified External Algo values")
        # endregion
