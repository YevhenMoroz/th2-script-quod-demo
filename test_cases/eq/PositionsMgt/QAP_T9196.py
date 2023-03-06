import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T9196(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')
        self.washbook_acc = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.order_submit = NewOrderReplyOMS(data_set).set_unsolicited_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create order
        self.order_submit.update_fields_in_component("NewOrderReplyBlock",
                                                     {"VenueAccount": {"VenueActGrpName": self.client}})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_rep = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        last_venue_ord_id = ord_rep["LastVenueOrdID"]
        self.ja_manager.compare_values({"WashBookAccountID": self.washbook_acc}, ord_rep, "Check WashBookAccountID")
        posit_qty = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value, [self.washbook_acc, JavaApiFields.PositQty.value]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]["PositQty"]
        # endregion
        # region Execute order
        self.exec_rep.set_default_trade(ord_rep["OrdID"])
        self.exec_rep.update_fields_in_component("ExecutionReportBlock", {"LastVenueOrdID": last_venue_ord_id})
        self.ja_manager.send_message_and_receive_response(self.exec_rep)
        posit = self.ja_manager.get_first_message(PKSMessageType.PositionReport.value, ).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        exp_posit_qty = str(float(posit_qty) + 100)
        self.ja_manager.compare_values({"PositQty": exp_posit_qty}, posit, "Check PositQty decreased")
        # endregion
