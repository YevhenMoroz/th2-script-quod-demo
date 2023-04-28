import datetime
import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, PositionValidities
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.pks_messages.RetailPositionConversionRequest import \
    RetailPositionConversionRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T3706(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pos_3_venue_1')
        self.client = self.data_set.get_client_by_name("client_pos_3")
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.account = self.data_set.get_account_by_name('client_pos_3_acc_4')
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.qty = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.OrdQty.value]
        self.instr_id = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.InstrID.value]
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.order_modify = OrderModificationRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.retail_position_conversion_request = RetailPositionConversionRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1: Create DMA orders
        pos_validity_list = [PositionValidities.PosValidity_DEL.value, PositionValidities.PosValidity_TP1.value]
        route_params = {JavaApiFields.RouteBlock.value: [{JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.AccountGroupID.value: self.client,
                                                      JavaApiFields.RouteList.value: route_params,
                                                      JavaApiFields.PreTradeAllocationBlock.value: {
                                                          JavaApiFields.PreTradeAllocationList.value: {
                                                              JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                                  {JavaApiFields.AllocAccountID.value: self.account,
                                                                   JavaApiFields.AllocQty.value: self.qty}]}}})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            for pos_validity in pos_validity_list:
                self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                             {JavaApiFields.AccountGroupID.value: self.client,
                                                              JavaApiFields.ClOrdID.value: bca.client_orderid(9),
                                                              JavaApiFields.PosValidity.value: pos_validity,
                                                              })
                self.ja_manager.send_message_and_receive_response(self.order_submit)
                order_reply = self.ja_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
                self.ja_manager.compare_values({JavaApiFields.PosValidity.value: pos_validity},
                                               order_reply,
                                               f'Verify that order has {JavaApiFields.PosValidity.value} equals {pos_validity}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 2: Perform "After Validity" option
        date = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime('%Y%m%d')
        result_before = self.db_manager.execute_query(f"SELECT COUNT(*) FROM retailposit WHERE alive = 'Y' AND instrid = '{self.instr_id}' AND accountid = '{self.account}'")
        self.ja_manager.compare_values({'CountOfRetailPosit': 2},
                                       {'CountOfRetailPosit': result_before[0][0]},
                                       f'Verify that 2 retaiposit exist for {self.account} (step 2)')
        self.retail_position_conversion_request.set_default(self.instr_id, self.account, date)
        self.ja_manager.send_message(self.retail_position_conversion_request)
        result_after = self.db_manager.execute_query(f"SELECT COUNT(*) FROM retailposit WHERE alive = 'Y' AND instrid = '{self.instr_id}' AND accountid='{self.account}'")
        self.ja_manager.compare_values({'CountOfRetailPosit': 1},
                                       {'CountOfRetailPosit': result_after[0][0]},
                                       f'Verify that only 1 retaiposit exist for {self.account} (step 2)')
        # endregion