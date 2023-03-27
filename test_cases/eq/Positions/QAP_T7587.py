import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7587(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_3_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.source_acc = self.data_set.get_account_by_name("client_pos_3_acc_2")
        self.dest_acc = self.data_set.get_account_by_name("client_pos_3_acc_3")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.pos_trans = PositionTransferInstructionOMS(data_set)
        self.request_for_position = RequestForPositions()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"PreTradeAllocationBlock": {
            "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                {"AllocAccountID": self.source_acc, "AllocQty": self.qty}]}}, "AccountGroupID": self.client})
        try:
            trd_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, float(self.price),
                                                                                          int(self.qty), True)
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trd_rule)

        # region Step 1-2
        result_for_wb1 = self._extract_cum_values_for_washbook(self.source_acc)
        result_for_wb2 = self._extract_cum_values_for_washbook(self.dest_acc)
        # endregion
        # region Step 3-4
        self.pos_trans.set_default_transfer(self.source_acc, self.dest_acc, self.qty)
        self.pos_trans.update_fields_in_component("PositionTransferInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name('instrument_1')})
        self.ja_manager.send_message_and_receive_response(self.pos_trans)
        trans_id = self.ja_manager.get_last_message(ORSMessageType.PositionTransferReport.value).get_parameters()[
            "PositionTransferReportBlock"]["PositionTransferID"]
        exec = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value, trans_id).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        # endregion
        # region Step 5-7
        result_for_wb1_new = self._extract_cum_values_for_washbook(self.source_acc)
        result_for_wb2_new = self._extract_cum_values_for_washbook(self.dest_acc)
        exp_res = str(float(result_for_wb1["PositQty"]) - float(self.qty))
        exp_res2 = str(float(result_for_wb2["PositQty"]) + float(self.qty))
        self.ja_manager.compare_values({"PositQty": exp_res}, result_for_wb1_new, "Step 5")
        self.ja_manager.compare_values({"PositQty": exp_res2}, result_for_wb2_new, "Step 6")
        self.ja_manager.compare_values({"ExecQty": str(float(self.qty))}, exec, "Step 7")
        # endregion

    def _extract_cum_values_for_washbook(self, washbook):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              washbook)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
