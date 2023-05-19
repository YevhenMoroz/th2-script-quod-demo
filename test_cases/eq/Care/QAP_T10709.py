import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    ExecutionPolicyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10709(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.new_order = OrderSubmitOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create CO order
        self.new_order.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                              desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                              role=SubmitRequestConst.USER_ROLE_1.value)
        self.new_order.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.AccountGroupID.value: self.client,
        })
        self.java_api_manager.send_message_and_receive_response(self.new_order)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verify that order is Open (step 1)')
        # endregion

        # region step 2: Split CO order
        self.new_order.set_default_child_dma(order_id)
        self.new_order.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                  {
                                                      JavaApiFields.AccountGroupID.value: self.client,
                                                  })
        price = self.new_order.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        ord_qty = self.new_order.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.OrdQty.value]
        new_order_single = child_ord_id = None
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.venue_client_names,
                self.venue,
                float(price))
            self.java_api_manager.send_message_and_receive_response(self.new_order)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                 ExecutionPolicyConst.DMA.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            child_ord_id = order_reply[JavaApiFields.OrdID.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Verify that order is Open (step 1)')
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(new_order_single)
        # endregion

        # region step 3: Partially Fill child DMA order
        filter_dict = {child_ord_id: child_ord_id}
        self.execution_report.set_default_trade(child_ord_id)
        half_qty = str(float(ord_qty) / 2)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             JavaApiFields.LastTradedQty.value: half_qty,
                                                             JavaApiFields.LastPx.value: price,
                                                             JavaApiFields.OrdType.value: "Limit",
                                                             JavaApiFields.Price.value: price,
                                                             JavaApiFields.LeavesQty.value: half_qty,
                                                             JavaApiFields.CumQty.value: half_qty,
                                                             JavaApiFields.AvgPrice.value: price,
                                                             JavaApiFields.OrdQty.value: ord_qty
                                                         })
        venue_exec_id = self.execution_report.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.VenueExecID.value]
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_dict)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report, 'Verify that child DMA order partially filled (step 3)')
        # endregion

        # region step 4: Send TradeCorrect ExecutionReport
        new_price = str(float(price) - 2)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.LastPx.value: new_price,
                                                             JavaApiFields.VenueExecRefID.value: venue_exec_id,
                                                             JavaApiFields.VenueExecID.value: bca.client_orderid(9),
                                                             JavaApiFields.TransactTime.value: (
                                                                     tm(datetime.utcnow().isoformat()) + bd(
                                                                 n=2)).date().strftime(
                                                                 '%Y-%m-%dT%H:%M:%S'),
                                                             JavaApiFields.ExecType.value: "TradeCorrect"
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report, filter_dict)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_second = execution_report[JavaApiFields.ExecID.value]
        time.sleep(1)
        # endregion

        second_exec = \
            self.db_manager.execute_query(
                f"SELECT execactive,execunmatchedqty,execprice,exectype FROM execution  WHERE execid='{exec_id_second}'")[0]
        first_exec = \
            self.db_manager.execute_query(f"SELECT execactive, execunmatchedqty FROM execution WHERE execid='{exec_id}'")[0]
        print(second_exec)
        print(first_exec)
        self.java_api_manager.compare_values({JavaApiFields.UnmatchedQty.value: '0.0',
                                              JavaApiFields.ExecPrice.value: new_price,
                                              JavaApiFields.ExecType.value: OrderReplyConst.ExecType_COR.value},
                                             {JavaApiFields.UnmatchedQty.value: str(float(second_exec[1])),
                                              JavaApiFields.ExecPrice.value: str(float(second_exec[2])),
                                              JavaApiFields.ExecType.value: second_exec[3]},
                                             'Verify that new DMA execution has properly values')
        self.java_api_manager.compare_values({'Alive': 'N',
                                              JavaApiFields.UnmatchedQty.value: '0.0'},
                                             {'Alive': first_exec[0],
                                              JavaApiFields.UnmatchedQty.value: str(float(first_exec[1]))},
                                             'Verify that old DMA execution has properly values')
