import logging
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, PKSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7602(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.client2 = self.data_set.get_client_by_name("client_pos_1")
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.environment.get_list_fe_environment()[0].user_1, self.desk, SubmitRequestConst.USER_ROLE_1.value)
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")['OrdQty']
        self.instr = self.order_submit.get_parameter("NewOrderSingleBlock")['InstrID']
        self.firm_account = self.data_set.get_account_by_name('client_pos_3_acc_3')  # PROP
        self.firm_account2 = self.data_set.get_account_by_name('client_pos_3_acc_2')  # Prime_Optimise
        self.wash_book = self.data_set.get_washbook_account_by_name('washbook_account_2')
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.request_for_position = RequestForPositions()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition

        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client,
                                                                             "PreTradeAllocationBlock": {
                                                                                 "PreTradeAllocationList": {
                                                                                     "PreTradeAllocAccountBlock":
                                                                                         [{
                                                                                             "AllocAccountID": self.firm_account,
                                                                                             "AllocQty": self.qty}]}}})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        order_id = ord_notif[JavaApiFields.OrdID.value]
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)

        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"ClOrdID": bca.client_orderid(9),
                                                                             "PreTradeAllocationBlock": {
                                                                                 "PreTradeAllocationList": {
                                                                                     "PreTradeAllocAccountBlock": [
                                                                                         {
                                                                                             "AllocAccountID": self.firm_account2,
                                                                                             "AllocQty": self.qty}]}}})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        order_id = ord_notif[JavaApiFields.OrdID.value]
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        # endregion
        # region Step 1 2
        cum_sell_qty_acc1 = self._get_cum_qty(self.firm_account)
        cum_sell_qty_acc2 = self._get_cum_qty(self.firm_account2)
        # endregion
        # region Step 3
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client2,
                                                                             "ClOrdID": basic_custom_actions.client_orderid(
                                                                                 9)})
        self.order_submit.remove_fields_from_component("NewOrderSingleBlock", ["PreTradeAllocationBlock"])
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_id = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion
        # region Step 4
        cum_buy_qty_wb = self._get_cum_qty(self.wash_book, "CumBuyQty")
        # endregion
        # region Step 5-6
        exec_qty = str(int(self.qty) // 2)
        self.trade_entry.set_default_house_fill(ord_id, self.firm_account, self.price, exec_qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        # endregion
        # region Step 7-8
        self.trade_entry.set_default_house_fill(ord_id, self.firm_account2, self.price, exec_qty)
        self.ja_manager.send_message_and_receive_response(self.trade_entry)
        # endregion
        # region Step 9-11
        cum_sell_qty_acc1_new = self._get_cum_qty(self.firm_account)
        cum_sell_qty_acc2_new = self._get_cum_qty(self.firm_account2)
        cum_buy_qty_wb_new = self._get_cum_qty(self.wash_book, "CumBuyQty")
        cum_sell_qty_acc1_exp = str(float(cum_sell_qty_acc1) + int(exec_qty))
        cum_sell_qty_acc2_exp = str(float(cum_sell_qty_acc2) + int(exec_qty))
        cum_buy_qty_wb_exp = str(float(cum_buy_qty_wb) + int(self.qty))
        self.ja_manager.compare_values({"CumBuyQty": cum_sell_qty_acc2_exp}, {"CumBuyQty": cum_sell_qty_acc2_new},
                                       "Check Step 9")
        self.ja_manager.compare_values({"CumBuyQty": cum_sell_qty_acc1_exp}, {"CumBuyQty": cum_sell_qty_acc1_new},
                                       "Check Step 10")
        self.ja_manager.compare_values({"CumBuyQty": cum_buy_qty_wb_exp}, {"CumBuyQty": cum_buy_qty_wb_new},
                                       "Check Step 11")
        # endregion

    def _get_cum_qty(self, account, type_qty="CumSellQty"):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value, account)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        posit_block_list = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value]
        for posit_block in posit_block_list:
            if account == posit_block["AccountID"] and self.instr == posit_block["InstrID"]:
                return posit_block[type_qty]
