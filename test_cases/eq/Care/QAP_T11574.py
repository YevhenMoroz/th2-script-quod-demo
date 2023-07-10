import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst, \
    OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T11574(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.manual_execute = TradeEntryOMS(self.data_set)
        self.fix_env = self.environment.get_list_fix_environment()[0]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create  CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.ja_manager.send_message_and_receive_response(self.order_submit, response_time=20_000)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                       order_reply, 'Verify that order created and has properly status (step 1)')
        ord_qty = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        half_qty = str(float(float(ord_qty) / 2))
        # endregion

        # region steps 2-5: Manual Execute CO:
        list_of_last_capacity = [ExecutionReportConst.LastCapacity_Mixed_FULL_VALUE.value,
                                 ExecutionReportConst.LastCapacity_CrossAsMixed_FULL_VALUE.value]
        self.manual_execute.set_default_trade(order_id, exec_qty=half_qty)
        trans_exec_status = [ExecutionReportConst.TransExecStatus_PFL.value,
                             ExecutionReportConst.TransExecStatus_FIL.value]
        for last_capacity in list_of_last_capacity:
            self.manual_execute.update_fields_in_component(JavaApiFields.TradeEntryRequestBlock.value,
                                                           {
                                                               JavaApiFields.LastCapacity.value: last_capacity
                                                           })
            self.ja_manager.send_message_and_receive_response(self.manual_execute)

            execution_report = self.ja_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
            self.ja_manager.compare_values({JavaApiFields.LastCapacity.value: last_capacity,
                                            JavaApiFields.TransExecStatus.value: trans_exec_status[
                                                list_of_last_capacity.index(last_capacity)]},
                                           execution_report,
                                           f'Verify that {execution_report[JavaApiFields.ExecID.value]} has properly {JavaApiFields.LastCapacity.value} and CO order has properly status (steps 3-5 )')
        # endregion
