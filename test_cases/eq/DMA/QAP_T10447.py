import logging
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10447(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)

        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.fix_verifier_bs = FixVerifier(self.environment.get_list_fix_environment()[0].buy_side, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.nos = NewOrderReplyOMS(self.data_set).set_unsolicited_dma_limit()
        self.exec_rep = ExecutionReportOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_es.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_esbuyTH2test.xml"

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Create Unsolicited Order
        self.nos.update_fields_in_component(JavaApiFields.NewOrderReplyBlock.value,
                                            {JavaApiFields.VenueAccount.value: {JavaApiFields.VenueActGrpName.value:
                                                                                    self.venue_client_names}})
        self.java_api_manager.send_message_and_receive_response(self.nos)

        ord_rep = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = ord_rep[JavaApiFields.OrdID.value]
        cl_ord_id = ord_rep[JavaApiFields.ClOrdID.value]
        ord_qty = str(float(ord_rep[JavaApiFields.OrdQty.value]))
        ord_venue_id = self.nos.get_parameter(JavaApiFields.NewOrderReplyBlock.value)[
            JavaApiFields.LastVenueOrdID.value]
        expected_result = {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                           JavaApiFields.UnsolicitedOrder.value: "Y"}
        self.java_api_manager.compare_values(expected_result, ord_rep, 'Check that order order ')
        # endregion

        # region step 2: Partially Filled Unsolicited order
        self.exec_rep.set_default_trade(cl_ord_id)
        half_qty = str(float(ord_qty) / 2)
        self.exec_rep.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value, {
            JavaApiFields.OrdQty.value: ord_qty,
            JavaApiFields.LastVenueOrdID.value: ord_venue_id,
            JavaApiFields.LastTradedQty.value: half_qty,
            JavaApiFields.LeavesQty.value: half_qty,
            JavaApiFields.CumQty.value: half_qty})
        filter_dict = {order_id: order_id}
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, filter_dict)
        execution_report_second_step = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        price = execution_report_second_step[JavaApiFields.Price.value]
        venue_exec_id_first = self.exec_rep.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.VenueExecID.value]
        day_cum_amt_first = str(float(half_qty) * float(price))
        self.java_api_manager.compare_values(
            {JavaApiFields.DayCumAmt.value: day_cum_amt_first,
             JavaApiFields.DayCumQty.value: half_qty},
            execution_report_second_step,
            f'Verifying that {JavaApiFields.DayCumQty.value} and {JavaApiFields.DayCumQty.value} has properly valeus (step 2)')
        # endregion

        # region step 3: send Fill message:
        venue_exec_id_second = bca.client_orderid(9)
        self.exec_rep.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value, {
            JavaApiFields.VenueExecID.value: venue_exec_id_second
        })
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, filter_dict)
        execution_report_thirth_step = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        day_cum_amt_second = str(float(ord_qty) * float(price))
        self.java_api_manager.compare_values(
            {JavaApiFields.DayCumAmt.value: day_cum_amt_second,
             JavaApiFields.DayCumQty.value: ord_qty},
            execution_report_thirth_step,
            f'Verifying that {JavaApiFields.DayCumQty.value} and {JavaApiFields.DayCumQty.value} has properly valeus (step 3)')
        # endregion

        # region step 4: send TradeCancel request for FirstExecution
        self._cancel_executions(half_qty, price, execution_report_second_step, venue_exec_id_first, filter_dict, ord_venue_id, 'step 4')
        # endregion

        # region step 5: send TradeCancel request for second Execution
        self._cancel_executions('0.0', price, execution_report_second_step, venue_exec_id_first, filter_dict,
                                ord_venue_id, 'step 5')
        # endregion

        # region step 6:Fully Trade Unsolicited order
        venue_exec_id_fifth = bca.client_orderid(9)
        self.exec_rep.get_parameters().clear()
        self.exec_rep.set_default_trade(cl_ord_id)
        self.exec_rep.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value, {
            JavaApiFields.OrdQty.value: ord_qty,
            JavaApiFields.LastVenueOrdID.value: ord_venue_id,
            JavaApiFields.LastTradedQty.value: ord_qty,
            JavaApiFields.LeavesQty.value: ord_qty,
            JavaApiFields.CumQty.value: ord_qty,
            JavaApiFields.VenueExecID.value: venue_exec_id_fifth
        })
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, filter_dict)
        execution_report_sixth_step = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        day_cum_amt_second = str(float(ord_qty) * float(price))
        self.java_api_manager.compare_values(
            {JavaApiFields.DayCumAmt.value: day_cum_amt_second,
             JavaApiFields.DayCumQty.value: ord_qty},
            execution_report_sixth_step,
            f'Verifying that {JavaApiFields.DayCumQty.value} and {JavaApiFields.DayCumQty.value} has properly valeus (step 6)')
        # endregion

    def _cancel_executions(self, qty, price, execution_report, venue_exec_id, filter_dict, ord_venue_id, step):
        self.exec_rep.get_parameters().clear()
        venue_exec_id_second = bca.client_orderid(9)
        self.exec_rep.set_default_cancel_unsolicited_execution(execution_report, venue_exec_id,
                                                               self.venue_client_names, ord_venue_id,
                                                               venue_exec_id_second)
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, filter_dict)
        execution_report_fourth_step = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        day_cum_amt = str(float(qty) * float(price))
        self.java_api_manager.compare_values(
            {JavaApiFields.DayCumAmt.value: day_cum_amt,
             JavaApiFields.DayCumQty.value: qty},
            execution_report_fourth_step,
            f'Verifying that {JavaApiFields.DayCumQty.value} and {JavaApiFields.DayCumQty.value} has properly valeus ({step})')