import logging
import os
import time
from pathlib import Path
import xml.etree.ElementTree as ET
from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionPolicyConst, \
    SubmitRequestConst, TimeInForces
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7114(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.manual_cross = ManualOrderCrossRequest()
        self.last_mkt = self.data_set.get_mic_by_name('mic_1')
        self.manual_cross_price = '10.0'
        self.manual_cross_mod_price = '15.0'
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition part 1: Set up needed config
        tree = ET.parse(self.local_path)
        element = ET.fromstring("<TradeCapture><autoCreation><enabled>true</enabled>"
                                "<venues><PARIS><enabled>true</enabled>""</PARIS></venues>"
                                "</autoCreation><sendToGateway>true</sendToGateway>"
                                "<Observers><FrontEnd><AccountMgrDeskID><Id>-1</Id><enabled>false</enabled>"
                                "</AccountMgrDeskID></FrontEnd></Observers>"
                                "<AccountGroup><enabled>true</enabled><id>SBK</id></AccountGroup></TradeCapture>")
        quod = tree.getroot().find("ors")
        quod.append(element)
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(50)
        # endregion

        # region precondition part 2: Create 2 CO orders with opposite side
        orders_ids = []
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.TimeInForce.value: TimeInForces.GTC.value
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        orders_ids.append(self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                              JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.Side.value: 'Sell',
                                                      JavaApiFields.ClOrdID.value: bca.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        orders_ids.append(self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                              JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])
        # endregion

        # region step 1-2: Manual Cross orders
        self.manual_cross.set_default(self.data_set, orders_ids[0], orders_ids[1], self.manual_cross_price)
        self.manual_cross.update_fields_in_component(JavaApiFields.ManualOrderCrossRequestBlock.value,
                                                     {JavaApiFields.ReportVenueID.value: "PARIS",
                                                      JavaApiFields.TradePublishIndicator.value: 'PTR',
                                                      JavaApiFields.TargetAPA.value: "LUK",
                                                      JavaApiFields.LastMkt.value: self.last_mkt,
                                                      JavaApiFields.AssistedReportAPA.value: "NAS",
                                                      JavaApiFields.OnExchangeRequested.value: "ONR",
                                                      })
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        manual_order_cross_id = \
            self.java_api_manager.get_last_message(ORSMessageType.ManualOrderCrossReply.value).get_parameters()[
                JavaApiFields.ManualOrderCrossReplyBlock.value][JavaApiFields.ManualOrderCrossID.value]
        self._check_values_of_trade_report('NEW', self.manual_cross_price, 'step 2', orders_ids)
        # endregion

        # region step 3-4: Modify manual cross
        self.manual_cross.update_fields_in_component(JavaApiFields.ManualOrderCrossRequestBlock.value,
                                                     {JavaApiFields.ManualOrderCrossTransType.value: 'REP',
                                                      JavaApiFields.ExecPrice.value: self.manual_cross_mod_price,
                                                      JavaApiFields.ManualOrderCrossID.value: manual_order_cross_id})
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        exec_ids = self._check_values_of_trade_report('REP', self.manual_cross_mod_price, 'step 4', orders_ids)
        # endregion

        # region step 5-6: Cancel Manual Cross
        self.manual_cross.update_fields_in_component(JavaApiFields.ManualOrderCrossRequestBlock.value, {
            JavaApiFields.ManualOrderCrossTransType.value: 'CAN'
        })
        self.java_api_manager.send_message_and_receive_response(self.manual_cross)
        self._check_values_of_trade_report('CAN', '0.0', 'step 6', orders_ids)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(50)
        os.remove("temp.xml")
        self.ssh_client.close()

    def _check_values_of_trade_report(self, trade_report_trans_type, exec_price, step, orders_ids=None):
        exec_id_first = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                       orders_ids[0]).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        exec_id_second = \
                self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                       orders_ids[1]).get_parameters()[
                    JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        execution_ids_list = [exec_id_first, exec_id_second]
        for exec_id in execution_ids_list:
            trade_entry_notif = self.java_api_manager.get_last_message(ORSMessageType.TradeCaptureReportNotif.value,
                                                                       exec_id).get_parameters()[
                JavaApiFields.TradeCaptureReportNotifBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.ExecPrice.value: exec_price,
                                                  JavaApiFields.TradeReportTransType.value: trade_report_trans_type},
                                                 trade_entry_notif,
                                                 f'Verify that trade report {trade_entry_notif[JavaApiFields.TradeReportID.value]} has properly values ({step})')
        return execution_ids_list
