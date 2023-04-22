import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.PositionTransferInstructionOMS import \
    PositionTransferInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7598(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn,
                                               self.test_id)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_submit = OrderSubmitOMS(data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.request_for_position = RequestForPositions()
        self.qty_to_trans = '100'
        self.source_acc = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.qty = '500'
        self.price = '2'
        self.client = self.data_set.get_client_by_name('client_pos_3')
        self.acc_to_trans = self.data_set.get_account_by_name('client_pos_3_acc_2')
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.pos_trans = PositionTransferInstructionOMS(data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        order_id = self._create_orders({
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.AccountGroupID.value: self.client})
        # endregion

        # region execute order
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_second_order = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.CumQty.value: str(float(self.qty))},
            execution_second_order, 'Check order execution')
        # endregion

        # region step 1: get postion for Security Account PROP
        position_before_trans_for_acc_prop = self._extract_cum_values_for_acc(self.source_acc)
        posit_qty_for_acc_prop = position_before_trans_for_acc_prop[JavaApiFields.PositQty.value]
        # endregion

        # region step 1: get postion for Security Account Prime_Optimise
        position_before_trans_for_acc_prime = self._extract_cum_values_for_acc(self.acc_to_trans)
        posit_qty_for_acc_prime = position_before_trans_for_acc_prime[JavaApiFields.PositQty.value]
        # endregion

        # region step 2-3: PositionTransfer
        self.pos_trans.set_default_transfer(self.source_acc, self.acc_to_trans, self.qty_to_trans)
        self.pos_trans.update_fields_in_component("PositionTransferInstructionBlock", {
            'InstrID': self.data_set.get_instrument_id_by_name('instrument_1')})
        self.java_api_manager.send_message_and_receive_response(self.pos_trans)
        # endregion

        # region step 4 : Check changes in Firm Positions Prime_Optimise
        position_for_prime_opt_qty_after_transfer = self._extract_cum_values_for_acc(self.acc_to_trans)
        posit_qty_for_prime_opt_qty_after_transfer = \
            position_for_prime_opt_qty_after_transfer[JavaApiFields.PositQty.value]
        increment_qty = str(abs(float(posit_qty_for_prime_opt_qty_after_transfer) - float(
            posit_qty_for_acc_prime)))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.PositQty.value}': str(float(self.qty_to_trans))},
            {f'Increment{JavaApiFields.PositQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.PositQty.value} increased on {self.qty_to_trans} for Prime_Optimise (step 4)')
        # endregion

        # region step 5 : Check changes in Firm Positions PROP
        position_for_prime_opt_qty_after_transfer = self._extract_cum_values_for_acc(self.source_acc)
        posit_qty_for_prop_qty_after_transfer = \
            position_for_prime_opt_qty_after_transfer[JavaApiFields.PositQty.value]
        decrement_qty = str(abs(float(posit_qty_for_prop_qty_after_transfer) - float(
            posit_qty_for_acc_prop)))
        self.java_api_manager.compare_values(
            {f'Decrement{JavaApiFields.PositQty.value}': str(float(self.qty_to_trans))},
            {f'Decrement{JavaApiFields.PositQty.value}': decrement_qty},
            f'Verifying that {JavaApiFields.PositQty.value} decreased on {self.qty_to_trans} for PROP (step 5)')
        # endregion

    def _create_orders(self, dictionary_with_needed_tags):
        self.order_submit = OrderSubmitOMS(self.data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", dictionary_with_needed_tags)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply,
                                             'Verifying that CO order created (Precondition)')
        return order_id

    def _extract_cum_values_for_acc(self, account):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              account)
        self.java_api_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.java_api_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record
