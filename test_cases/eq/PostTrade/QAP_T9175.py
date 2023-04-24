import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T9175(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')

        self.order_submit = NewOrderReplyOMS(data_set).set_unsolicited_dma_limit()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create order
        misc_block = {"OrdrMisc0": "test"}
        self.order_submit.update_fields_in_component("NewOrderReplyBlock",
                                                     {"VenueAccount": {"VenueActGrpName": self.client},
                                                      "OrdrMiscBlock":misc_block })
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_rep = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values(misc_block,ord_rep["OrdrMiscBlock"],"Step 1")
        # endregion

