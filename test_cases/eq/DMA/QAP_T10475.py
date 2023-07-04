import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdTypes, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.es_messages.OrdReportOMS import OrdReportOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10475(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.new_order_reply = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.order_report = OrdReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create Unsolicited order
        last_venue_ord_id = self.new_order_reply.get_parameters()[JavaApiFields.NewOrderReplyBlock.value][JavaApiFields.LastVenueOrdID.value]
        self.new_order_reply.update_fields_in_component(JavaApiFields.NewOrderReplyBlock.value,
                                                        {
                                                            JavaApiFields.OrdType.value: OrdTypes.StopLimit.value,
                                                        })
        self.java_api_manager.send_message_and_receive_response(self.new_order_reply)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdType.value: OrdTypes.StopLimit.value,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that order unsolicited has properly values (step 1)')
        order_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # region step 2: Send OrdReport
        self.order_report.set_default_open(order_id, last_venue_ord_id)
        self.order_report.update_fields_in_component(JavaApiFields.OrdReportBlock.value, {
            JavaApiFields.ExecType.value: OrderReplyConst.ExecType_RES.value
        })
        self.java_api_manager.send_message_and_receive_response(self.order_report)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that order unsolicited has properly values (step 2)')
        # endregion
