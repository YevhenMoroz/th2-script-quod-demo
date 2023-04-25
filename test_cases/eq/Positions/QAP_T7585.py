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
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7585(TestCase):
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
        self.qty_for_check = '200'
        self.qty_for_first_hf = '50'
        self.qty_for_second_hf = '70'
        self.source_acc = self.data_set.get_account_by_name('client_pos_3_acc_1')
        self.price = '2'
        self.client = self.data_set.get_client_by_name('client_pos_1')
        self.care_washbook = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.trade_entry = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 2: Create CO order
        order_id = self._create_orders({
            JavaApiFields.OrdQty.value: self.qty_for_check,
            JavaApiFields.Price.value: self.price,
            JavaApiFields.AccountGroupID.value: self.client,
            "WashBookAccountID": self.care_washbook})
        # endregion

        # region step 3: get postion for Source Account and Security Account
        position_before_trading_for_washbook = self._extract_cum_values_for_washbook(self.care_washbook)
        cumm_buy_qty_position_before_trading_for_washbook = position_before_trading_for_washbook[
            JavaApiFields.CumBuyQty.value]
        posit_qty_for_washbook = position_before_trading_for_washbook[JavaApiFields.PositQty.value]
        position_before_trading_for_source_acc = self._extract_cum_values_for_washbook(self.source_acc)
        cumm_sell_qty_before_trade_for_source_account = position_before_trading_for_source_acc[
            JavaApiFields.CumSellQty.value]
        posit_qty_for_source_acc = position_before_trading_for_source_acc[JavaApiFields.PositQty.value]
        # endregion

        # region step 4: Trade CO order via House Fill
        self.trade_entry.set_default_trade(order_id, self.price, self.qty_for_first_hf)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {'SourceAccountID': self.source_acc})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_second_order = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.CumQty.value: str(float(self.qty_for_first_hf))},
            execution_second_order, 'Check CumQty for order after first House Fill (step 4)')
        # endregion

        # region step 5 : Check changes in Firm Positions
        position_after_trading_for_source_acc_after_trade = self._extract_cum_values_for_washbook(self.source_acc)
        cumm_sell_qty_after_trade_for_source_account_qty_after_trade = \
            position_after_trading_for_source_acc_after_trade[JavaApiFields.CumSellQty.value]
        increment_qty = str(float(cumm_sell_qty_after_trade_for_source_account_qty_after_trade) - float(
            cumm_sell_qty_before_trade_for_source_account))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.CumSellQty.value}': str(float(self.qty_for_first_hf))},
            {f'Increment{JavaApiFields.CumSellQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.CumSellQty.value} increased on {self.qty_for_first_hf} for Facilitation(step 5)')

        posit_qty_after_trade_for_source_account_qty_after_trade = \
            position_after_trading_for_source_acc_after_trade[JavaApiFields.PositQty.value]
        decrement_qty = str(float(posit_qty_for_source_acc) - float(
            posit_qty_after_trade_for_source_account_qty_after_trade))
        self.java_api_manager.compare_values(
            {f'Decrement{JavaApiFields.PositQty.value}': str(float(self.qty_for_first_hf))},
            {f'Decrement{JavaApiFields.PositQty.value}': decrement_qty},
            f'Verifying that {JavaApiFields.PositQty.value} decreased on {self.qty_for_first_hf} for Facilitation (step 5)')
        # endregion

        # region step 6 : Check changes in WashBook Position
        position_after_trading_for_washbook_after_trade = self._extract_cum_values_for_washbook(self.care_washbook)
        cumm_buy_qty_after_trade_for_washbook_qty_after_trade = \
            position_after_trading_for_washbook_after_trade[JavaApiFields.CumBuyQty.value]
        increment_qty = str(float(cumm_buy_qty_after_trade_for_washbook_qty_after_trade) - float(
            cumm_buy_qty_position_before_trading_for_washbook))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.CumBuyQty.value}': str(float(self.qty_for_first_hf))},
            {f'Increment{JavaApiFields.CumBuyQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.CumBuyQty.value} increased on {self.qty_for_first_hf} for CareWB (step 6)')

        posit_qty_after_trade_for_washbook_qty_after_trade = \
            position_after_trading_for_washbook_after_trade[JavaApiFields.PositQty.value]
        increment_qty = str(float(posit_qty_after_trade_for_washbook_qty_after_trade) - float(
            posit_qty_for_washbook))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.PositQty.value}': str(float(self.qty_for_first_hf))},
            {f'Increment{JavaApiFields.PositQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.PositQty.value} increased on {self.qty_for_first_hf} for CareWB (step 6)')
        # endregion

        # region step 7: Trade CO order via House Fill
        self.trade_entry.set_default_trade(order_id, self.price, self.qty_for_second_hf)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock', {'SourceAccountID': self.source_acc})
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        execution_second_order = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.CumQty.value: str(float(self.qty_for_first_hf) + float(self.qty_for_second_hf))},
            execution_second_order, 'Check CumQty for order after second House Fill (step 7)')
        # endregion

        # region step 8 : Check changes in Firm Positions
        position_after_trading_for_source_acc_after_trade2 = self._extract_cum_values_for_washbook(self.source_acc)
        cumm_sell_qty_after_trade_for_source_account_qty_after_trade2 = \
            position_after_trading_for_source_acc_after_trade2[JavaApiFields.CumSellQty.value]
        increment_qty = str(float(cumm_sell_qty_after_trade_for_source_account_qty_after_trade2) - float(
            cumm_sell_qty_after_trade_for_source_account_qty_after_trade))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.CumSellQty.value}': str(float(self.qty_for_second_hf))},
            {f'Increment{JavaApiFields.CumSellQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.CumSellQty.value} increased on {self.qty_for_second_hf} for Facilitation (step 8)')

        posit_qty_after_trade_for_source_account_qty_after_trade2 = \
            position_after_trading_for_source_acc_after_trade2[JavaApiFields.PositQty.value]
        decrement_qty = str(float(posit_qty_after_trade_for_source_account_qty_after_trade) - float(
            posit_qty_after_trade_for_source_account_qty_after_trade2))
        self.java_api_manager.compare_values(
            {f'Decrement{JavaApiFields.PositQty.value}': str(float(self.qty_for_second_hf))},
            {f'Decrement{JavaApiFields.PositQty.value}': decrement_qty},
            f'Verifying that {JavaApiFields.PositQty.value} decreased on {self.qty_for_second_hf} for Facilitation (step 8)')
        # endregion

        # region step 9 : Check changes in WashBook Position
        position_after_trading_for_washbook_after_trade2 = self._extract_cum_values_for_washbook(self.care_washbook)
        cumm_buy_qty_after_trade_for_washbook_qty_after_trade2 = \
            position_after_trading_for_washbook_after_trade2[JavaApiFields.CumBuyQty.value]
        increment_qty = str(float(cumm_buy_qty_after_trade_for_washbook_qty_after_trade2) - float(
            cumm_buy_qty_after_trade_for_washbook_qty_after_trade))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.CumBuyQty.value}': str(float(self.qty_for_second_hf))},
            {f'Increment{JavaApiFields.CumBuyQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.CumBuyQty.value} increased on {self.qty_for_check} for CareWB (step 9)')

        posit_qty_after_trade_for_washbook_qty_after_trade2 = \
            position_after_trading_for_washbook_after_trade2[JavaApiFields.PositQty.value]
        increment_qty = str(float(posit_qty_after_trade_for_washbook_qty_after_trade2) - float(
            posit_qty_after_trade_for_washbook_qty_after_trade))
        self.java_api_manager.compare_values(
            {f'Increment{JavaApiFields.PositQty.value}': str(float(self.qty_for_second_hf))},
            {f'Increment{JavaApiFields.PositQty.value}': increment_qty},
            f'Verifying that {JavaApiFields.PositQty.value} increased on {self.qty_for_second_hf} for CareWB (step 9)')
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
                                              JavaApiFields.WashBookAccountID.value: self.care_washbook},
                                             order_reply,
                                             'Verifying that CO order created and has CareWB (step 2)')
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
