import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubscriptionRequestTypes, PosReqTypes, \
    SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.position_calculation_manager import PositionCalculationManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7574(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_3_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.client2 = self.data_set.get_client_by_name("client_pos_1")
        self.acc1 = self.data_set.get_account_by_name("client_pos_3_acc_3")
        self.acc2 = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.request_for_position = RequestForPositions()
        self.pos_manager = PositionCalculationManager()
        self.trd_entry = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1,3
        result_for_acc1 = self._extract_cum_values_for_account(self.acc1)
        result_for_acc2 = self._extract_cum_values_for_account(self.acc2)
        # endregion
        # region Step 2
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"PreTradeAllocationBlock": {
            "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                {"AllocAccountID": self.acc1, "AllocQty": self.qty}]}}, "AccountGroupID": self.client})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion
        # region Step 4-5
        self.trd_entry.set_default_house_fill(order_id, self.acc2, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trd_entry)
        # endregion
        # region Step 6-8
        result_for_wb1_new = self._extract_cum_values_for_account(self.acc1)
        result_for_wb2_new = self._extract_cum_values_for_account(self.acc2)
        exp_pos_qty = str(float(result_for_acc1["PositQty"]) + float(self.qty))
        exp_pos_qty2 = str(float(result_for_acc2["PositQty"]) - float(self.qty))
        self.ja_manager.compare_values({"PositQty": exp_pos_qty}, result_for_wb1_new, "Step 6")
        self.ja_manager.compare_values({"PositQty": exp_pos_qty2}, result_for_wb2_new, "Step 7")
        # endregion

    def _extract_cum_values_for_account(self, washbook):
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
