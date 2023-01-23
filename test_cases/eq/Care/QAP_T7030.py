import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7030(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_type = OrderType.limit.value
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.dfd_manage_batch = DFDManagementBatchOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Create CO order
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        response = self.fix_manager.send_message_and_receive_response_fix_standard(nos)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region get values
        qty = nos.get_parameter('OrderQtyData')["OrderQty"]
        price = nos.get_parameter('Price')
        # endregion

        # region Manual Execution
        exp_day_cum_qty = qty
        exp_day_cum_amt = str(int(int(qty) * int(price)))
        self.trade_entry_request.set_default_trade(order_id, price)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check values after execution
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DayCumQty.value: exp_day_cum_qty + '.0',
                                              JavaApiFields.DayCumAmt.value: exp_day_cum_amt + '.0'}, exec_report_block,
                                             'Check DayCumQty and DayCumAmt after execution')
        # endregion

        # region complete order
        self.dfd_manage_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_manage_batch)
        # endregion

        # region check values after execution
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DayCumQty.value: exp_day_cum_qty + '.0',
                                              JavaApiFields.DayCumAmt.value: exp_day_cum_amt + '.0',
                                              JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
                                              JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value},
                                             ord_reply_block,
                                             'Check DayCumQty and DayCumAmt after completing')
        # endregion

        # region un-complete order
        self.dfd_manage_batch.set_default_uncomplete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_manage_batch)
        # endregion

        # region check values after execution
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.DayCumQty.value: exp_day_cum_qty + '.0',
                                              JavaApiFields.DayCumAmt.value: exp_day_cum_amt + '.0'},
                                             ord_reply_block,
                                             'Check DayCumQty and DayCumAmt after completing')
        # endregion
