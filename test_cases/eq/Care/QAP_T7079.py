import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, ExecutionReportConst, \
    OrderReplyConst, ExecutionPolicyConst, PositionValidities
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7079(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_modify = OrderModificationRequest()
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create CO order
        self.order_submit.set_default_care_market(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                  desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                  role=SubmitRequestConst.USER_ROLE_1.value)
        qty = '6000'
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.OrdQty.value: qty,
                                                      JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply,
                                             "Verify that order created")
        # end_of_part

        # region step 2: Split Order with External
        # part 1: Create child order
        self.order_submit.get_parameters().clear()
        self.order_submit.set_default_child_dma_market(parent_id=ord_id, external_algo_twap=True)
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.OrdQty.value: qty,
                                                      JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        child_order_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # part 2 trade child DMA order
        self.execution_report.set_default_trade(child_order_id)
        half_qty = str(float(qty) / 2)
        price = '20.0'
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {JavaApiFields.OrdQty.value: qty,
                                                          JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value,
                                                          JavaApiFields.LastTradedQty.value: half_qty,
                                                          JavaApiFields.LastPx.value: price,
                                                          JavaApiFields.Price.value: price,
                                                          JavaApiFields.LeavesQty.value: half_qty,
                                                          JavaApiFields.CumQty.value: half_qty,
                                                          JavaApiFields.AvgPrice.value: price})
        self.java_api_manager.send_message_and_receive_response(self.execution_report, {ord_id: ord_id})
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verify that order partially filled (step 2)')
        # endregion

        # region step 3 : Amend CO order
        new_qty = '8000.0'
        self.order_modify.set_default(self.data_set, ord_id)
        self.order_modify.update_fields_in_component(JavaApiFields.OrderModificationRequestBlock.value,
                                                     {
                                                         JavaApiFields.OrdType.value: 'Market',
                                                         JavaApiFields.TimeInForce.value: 'DAY',
                                                         JavaApiFields.OrdQty.value: new_qty,
                                                         JavaApiFields.BookingType.value: 'REG',
                                                         JavaApiFields.PosValidity.value: PositionValidities.PosValidity_DEL.value,
                                                         JavaApiFields.WashBookAccountID.value: self.data_set.get_washbook_account_by_name(
                                                             'washbook_account_3'),
                                                         JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.CARE.value,
                                                     })
        self.order_modify.remove_fields_from_component(JavaApiFields.OrderModificationRequestBlock.value,
                                                       [JavaApiFields.Price.value])
        modify_rule = False
        try:
            modify_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.fix_env.buy_side,
                                                                                      self.venue_client_name, self.mic,
                                                                                      True)
            self.java_api_manager.send_message_and_receive_response(self.order_modify,
                                                                    filter_dict={ord_id: ord_id, child_order_id: child_order_id})
        except Exception as e:
            logger.error(e)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(modify_rule)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id).get_parameters() \
            [JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdQty.value: new_qty},
                                             order_reply, f'Verify that CO order {ord_id} has new qty (step 3)')
        # endregion

        # region step 4: Amend DMA order:
        order_reply = \
        self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, child_order_id).get_parameters() \
            [JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdQty.value: new_qty},
                                             order_reply,
                                             f'Verify that DMA order {child_order_id} has new qty (step 4)')
        # endregion
