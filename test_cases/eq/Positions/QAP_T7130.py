import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7130(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_1_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.dest_acc = self.data_set.get_account_by_name("client_pos_3_acc_3")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.pos_trans = PositionTransferInstructionOMS(data_set)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.request_for_position = RequestForPositions()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self._subscription_on_position()
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.AccountGroupID.value: self.client,
                                                      JavaApiFields.WashBookAccountID.value: self.washbook})
        try:
            trd_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, float(self.price),
                                                                                          int(self.qty), True)
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(trd_rule)

        posit_qty = \
            self.ja_manager.get_last_message(PKSMessageType.PositionReport.value,
                                             JavaApiFields.PositQty.value).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0][JavaApiFields.PositQty.value]
        # endregion
        # region Step 3
        self.pos_trans.set_default_transfer(self.washbook, self.dest_acc, self.qty)
        self.pos_trans.update_fields_in_component(JavaApiFields.PositionTransferInstructionBlock.value,
                                                  {JavaApiFields.InstrID.value: self.data_set.get_instrument_id_by_name(
                                                      'instrument_1')})
        self.ja_manager.send_message_and_receive_response(self.pos_trans)
        posit_block = \
            self.ja_manager.get_first_message(PKSMessageType.PositionReport.value, self.washbook).get_parameters()[
                JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
                JavaApiFields.PositionBlock.value][0]
        exp_posit_qty = str(float(posit_qty) - int(self.qty))
        self.ja_manager.compare_values({JavaApiFields.PositQty.value: exp_posit_qty}, posit_block, "Check PositQty")
        # endregion

    def _subscription_on_position(self):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              self.washbook)
        self.ja_manager.send_message(self.request_for_position)