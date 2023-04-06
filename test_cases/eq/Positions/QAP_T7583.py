import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubscriptionRequestTypes, PosReqTypes, \
    SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.position_calculation_manager import PositionCalculationManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7583(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.environment.get_list_fe_environment()[0].user_1,
            self.environment.get_list_fe_environment()[0].desk_ids[0], SubmitRequestConst.USER_ROLE_1.value)
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.request_for_position = RequestForPositions()
        self.pos_trans = PositionTransferInstructionOMS(data_set)
        self.acc1 = self.data_set.get_account_by_name("client_pos_3_acc_2")  # "Prime_Optimise"
        self.acc2 = self.data_set.get_account_by_name("client_pos_3_acc_4")  # "PROP_TEST"
        self.pos_manager = PositionCalculationManager()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"PreTradeAllocationBlock": {
            "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                {"AllocAccountID": self.acc1, "AllocQty": self.qty}]}}, "AccountGroupID": self.client})
        try:
            trd_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, float(self.price),
                                                                                          int(self.qty), True)
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trd_rule)
        # endregion
        # region 1-2
        posit_acc1 = self._extract_cum_values_for_acc(self.acc1)
        posit_acc2 = self._extract_cum_values_for_acc(self.acc2)
        # endregion
        # region Step 3-4
        self.pos_trans.set_default_transfer(self.acc1, self.acc2, self.qty, self.price)
        self.pos_trans.update_fields_in_component("PositionTransferInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name('instrument_1')})
        self.ja_manager.send_message_and_receive_response(self.pos_trans)
        pos_report_acc2 = self.ja_manager.get_last_message(PKSMessageType.PositionReport.value,
                                                           self.acc2).get_parameters()["PositionReportBlock"][
            "PositionList"]["PositionBlock"][0]
        # endregion
        # region Step 5-8
        result_for_acc2_new = self._extract_cum_values_for_acc(self.acc2)
        ecp_pos_qty_acc2 = str(float(posit_acc2["PositQty"]) + float(self.qty))
        exp_net_weighted_avg_px_acc2 = self.pos_manager.calculate_gross_weighted_avg_px_buy_side(
            posit_acc2["NetWeightedAvgPx"], posit_acc2["PositQty"], self.qty, self.price)

        self.ja_manager.compare_values({"PositQty": ecp_pos_qty_acc2, "NetWeightedAvgPx": exp_net_weighted_avg_px_acc2},
                                       result_for_acc2_new, "check PositQty and NetWeightedAvgPx for PROP_TEST")

        result_for_acc1_new = self._extract_cum_values_for_acc(self.acc1)
        ecp_pos_qty_acc1 = str(float(posit_acc1["PositQty"]) - float(self.qty))
        self.ja_manager.compare_values({"PositQty": ecp_pos_qty_acc1},
                                       result_for_acc1_new, "check PositQty Prime_Optimise")
        mid_px = "35"
        exp_unrealized_pl = str((float(mid_px) - float(exp_net_weighted_avg_px_acc2)) * float(ecp_pos_qty_acc2))

        self.ja_manager.compare_values({"UnrealizedPL": exp_unrealized_pl}, pos_report_acc2,
                                       "check UnrealizedPL for PROP_TEST")
        # endregion

    def _extract_cum_values_for_acc(self, acc):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              acc)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
