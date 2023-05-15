import logging
import time
from datetime import datetime
from pathlib import Path

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

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
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T3662(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client = self.data_set.get_client_by_name("client_1")
        self.account = self.data_set.get_account_by_name('client_1_acc_3')
        self.instrument_id = self.data_set.get_instrument_id_by_name("instrument_1")
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bs_connectivity = self.fix_env.buy_side
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.exec_rep = ExecutionReportOMS(data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.qty = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.OrdQty.value]
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.order_modify = OrderModificationRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        self.db_manager.execute_query(
            f"UPDATE institution SET posflatteningtime='{(tm(datetime.utcnow().isoformat()) - bd(1)).date().strftime('%Y-%m-%dT%H:%M:%S')}' WHERE institutionname ='QUOD FINANCIAL 1'")
        self.ssh_client.send_command('qrestart all')
        time.sleep(180)
        # endregion
        # region Step 1 : Create DMA order
        route_params = {JavaApiFields.RouteBlock.value: [{JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.AccountGroupID.value: self.client,
                                                      JavaApiFields.RouteList.value: route_params,
                                                     JavaApiFields.PreTradeAllocationBlock.value: {
                                                          JavaApiFields.PreTradeAllocationList.value: {JavaApiFields.PreTradeAllocAccountBlock.value: [
                                                              {
                                                                  JavaApiFields.AllocAccountID.value: self.account,
                                                                  JavaApiFields.AllocQty.value: self.qty}]}},
                                                      JavaApiFields.PosValidity.value: PositionValidities.PosValidity_ITD.value})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  float(self.price))
            self.ja_manager.send_message_and_receive_response(self.order_submit)
            order_submit_reply = self.ja_manager.get_last_message(ORSMessageType.OrderSubmitReply.value).get_parameters()
            order_id = order_submit_reply[JavaApiFields.NewOrderReplyBlock.value][JavaApiFields.Ord.value][JavaApiFields.OrdID.value]
            block_for_verifying = order_submit_reply[JavaApiFields.MessageReply.value][JavaApiFields.MessageReplyBlock.value][0]
            self.ja_manager.compare_values({JavaApiFields.ErrorMsg.value: f"Invalid 'PosValidity': {order_id}"},
                                           block_for_verifying,
                                           f'Verify that error message present (step 2)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
