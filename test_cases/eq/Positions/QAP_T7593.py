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
    SubscriptionRequestTypes, PosReqTypes, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7593(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn,
                                               self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(self.wa_connectivity, self.test_id)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_submit = OrderSubmitOMS(data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.request_for_position = RequestForPositions()
        self.qty_for_check = '100'
        self.price = '2'
        self.client = self.data_set.get_client_by_name('client_1')
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.default_washbook = self.data_set.get_washbook_account_by_name('washbook_account_3')
        self.dma_washbook = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order
        cl_ord_id = bca.client_orderid(9)
        order_id = self._create_orders({
            JavaApiFields.OrdQty.value: self.qty_for_check,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value,
            JavaApiFields.AccountGroupID.value: self.client,
            "ClOrdID": cl_ord_id})
        # endregion

        # region step 2: get postion for default_washbook
        default_wb_position_before_trading = self._extract_cum_values_for_washbook(self.default_washbook)
        # endregion

        # region step  3-4 : Create and Trade Split DMA order
        trade_rule = None
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule,
                self.mic,
                float(self.price),
                traded_qty=int(self.qty_for_check),
                delay=0)
            self.order_submit.set_default_child_dma(order_id, bca.client_orderid(9))
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                JavaApiFields.WashBookAccountID.value: self.dma_washbook,
                JavaApiFields.Price.value: self.price,
                JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value,
                JavaApiFields.AccountGroupID.value: self.client,
            })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
        except Exception as e:
            logger.error(f'Your exception is {e}', exc_info=True)
        finally:
            self.rule_manager.remove_rule(trade_rule)
            execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
                execution_report,
                'Verifying that order fully filled (step 4)')
        # endregion

        # region step 5 : Check changes in WashBook
        cumm_sell_qty_before_trade = default_wb_position_before_trading[JavaApiFields.CumSellQty.value]
        order_position = self.java_api_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                                   [JavaApiFields.PositQty.value,
                                                                                    self.default_washbook]). \
            get_parameters()[JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        cumm_sell_qty_after_trade = order_position[JavaApiFields.CumSellQty.value]
        increment_qty = str(float(cumm_sell_qty_after_trade) - float(cumm_sell_qty_before_trade))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.CumSellQty.value}': str(float(self.qty_for_check))},
            {f'Increment{JavaApiFields.CumSellQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.CumSellQty.value} increased on {self.qty_for_check} for default washbook(step 5)')
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
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                              JavaApiFields.WashBookAccountID.value: self.default_washbook},
                                             order_reply,
                                             'Verifying that CO order created and has default washbook (step 1)')
        return order_id

    def _extract_cum_values_for_washbook(self, account):
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
