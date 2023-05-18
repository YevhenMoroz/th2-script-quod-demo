import logging
import os
import time
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
import xml.etree.ElementTree as ET
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import PKSMessageType, ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, \
    SubscriptionRequestTypes, PosReqTypes, SubmitRequestConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.pks_messages.RequestForPositions import RequestForPositions
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T3246(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_5_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_5")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.account = self.data_set.get_account_by_name('client_pos_5_acc_1')
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.qty = '100'
        self.qty_for_first_order = '120'
        self.instr_id = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[
            JavaApiFields.InstrID.value]
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.order_modify = OrderModificationRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.request_for_position = RequestForPositions()
        self.cash_account_id = self.data_set.get_cash_account_by_name('cash_account_id_client_posit_ret_sa_1')
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_backend.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_backend.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition part 1: DELETE posit records
        tree = ET.parse(self.local_path)
        tree.getroot().find("limits/buyingPower/enabled").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.db_manager.execute_query(
            f"DELETE FROM dailyposit WHERE accountid = '{self.account}'")
        self.db_manager.execute_query(f"DELETE from posit WHERE accountid = '{self.account}'")
        self.ssh_client.send_command('qrestart all')
        time.sleep(180)
        # endregion

        # region precondition part 2: Create DMA order (Side = Buy)
        route_params = {JavaApiFields.RouteBlock.value: [
            {JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.AccountGroupID.value: self.client,
                                                      JavaApiFields.RouteList.value: route_params,
                                                      JavaApiFields.OrdQty.value: self.qty_for_first_order,
                                                      JavaApiFields.CashAccountID.value: self.cash_account_id,
                                                      JavaApiFields.PreTradeAllocationBlock.value: {
                                                          JavaApiFields.PreTradeAllocationList.value: {
                                                              JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                                  {JavaApiFields.AllocAccountID.value: self.account,
                                                                   JavaApiFields.AllocQty.value: self.qty_for_first_order}]}}})
        self._trade_order(self._create_order)
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                       order_reply,
                                       'Verify that order created (precondition)')
        # endregion

        # region step 1-5
        result = self._extract_positions(self.account)
        self.ja_manager.compare_values({JavaApiFields.PositQty.value: self.qty_for_first_order},
                                       result,
                                       f'Make sure, that {JavaApiFields.PositQty.value}  == {self.qty_for_first_order} (step 2)')
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.ClOrdID.value: bca.client_orderid(9),
                                                      JavaApiFields.OrdQty.value: self.qty,
                                                      JavaApiFields.Side.value: SubmitRequestConst.Side_Sell.value})
        self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)\
            [JavaApiFields.PreTradeAllocationBlock.value][JavaApiFields.PreTradeAllocationList.value]\
            [JavaApiFields.PreTradeAllocAccountBlock.value][0][JavaApiFields.AllocQty.value] = self.qty
        self._create_order()
        order_reply = self.ja_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                       order_reply,
                                       'Verify that order created (step 5)')
        # endregion

        # region step 6: Check that LeavesSellQty increased
        position_report = self.ja_manager.get_last_message_by_multiple_filter(PKSMessageType.PositionReport.value,
                                                                              [JavaApiFields.LeavesSellQty.value,
                                                                               self.account,
                                                                               f"{JavaApiFields.PositionType.value}:'L'"]).get_parameters()[
            JavaApiFields.PositionReportBlock.value][JavaApiFields.PositionList.value][
            JavaApiFields.PositionBlock.value][0]
        self.ja_manager.compare_values({JavaApiFields.LeavesSellQty.value: self.qty},
                                       position_report,
                                       f'Verify that LeavesSellQty increased on {self.qty} (step 6)')
        # endregion

    def _extract_positions(self, firm_account):
        self.request_for_position.set_default(SubscriptionRequestTypes.SubscriptionRequestType_SUB.value,
                                              PosReqTypes.PosReqType_POS.value,
                                              firm_account)
        self.ja_manager.send_message_and_receive_response(self.request_for_position)
        request_for_position_ack = self.ja_manager.get_last_message(PKSMessageType.RequestForPositionsAck.value). \
            get_parameters()[JavaApiFields.RequestForPositionsAckBlock.value][JavaApiFields.PositionReportBlock.value] \
            [JavaApiFields.PositionList.value][JavaApiFields.PositionBlock.value]
        for position_record in request_for_position_ack:
            if self.instrument_id == position_record[JavaApiFields.InstrID.value]:
                return position_record

    def _create_order(self):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

    def _trade_order(self, function):
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_name,
                                                                                            self.mic,
                                                                                            float(self.price),
                                                                                            int(self.qty_for_first_order), 0)
            function()
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        time.sleep(180)
        os.remove("temp.xml")
