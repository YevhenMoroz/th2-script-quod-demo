import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixDontKnowTrade import FixDontKnowTrade
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T11703(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)

        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fe_env = self.environment.get_list_fe_environment()[0]
        self.fix_verifier_bs = FixVerifier(self.environment.get_list_fix_environment()[0].buy_side, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.exec_rep = ExecutionReportOMS(self.data_set)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs",
                                            "client_es.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_es.xml"
        self.ord_submit = OrderSubmitOMS(self.data_set)
        self.new_order_reply = NewOrderReplyOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("es/execution/supportDontKnowTrade").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ESBUYTH2TEST")
        time.sleep(60)
        # endregion

        # region step 1: create DMA order
        self.ord_submit.set_default_dma_limit()
        self.java_api_manager.send_message_and_receive_response(self.ord_submit)
        ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             ord_reply,
                                             f'Verify that order has Sts = "{OrderReplyConst.TransStatus_SEN.value} (step 1)"')
        order_id = ord_reply[JavaApiFields.OrdID.value]
        price = ord_reply[JavaApiFields.Price.value]
        qty = ord_reply[JavaApiFields.OrdQty.value]
        # endregion

        # region step 2: Send 35 = 8 (New Order Reply message) message
        self.new_order_reply.set_default_dma_limit(order_id)
        self.java_api_manager.send_message(self.new_order_reply)
        status = \
            self.db_manager.execute_query(
                f"SELECT exectype FROM ordreply WHERE transid='{order_id}' AND exectype='{OrderReplyConst.ExecType_OPN.value}'")[
                0][0]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             {JavaApiFields.TransStatus.value: status},
                                             'Verify that order is being Open now (step 2)')
        # endregion

        # region step 3: Send 35 = 8 (Fully Fill message)
        self.exec_rep.set_default_trade(order_id)
        new_price = str(float(price) + 2)
        venue_exec_id = self.exec_rep.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.VenueExecID.value]
        last_venue_ord_id = self.exec_rep.get_parameters()[JavaApiFields.ExecutionReportBlock.value][
            JavaApiFields.LastVenueOrdID.value]
        self.exec_rep.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                 {JavaApiFields.LastPx.value: new_price})
        self.java_api_manager.send_message_and_receive_response(self.exec_rep)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.LeavesQty.value: str(float(qty))},
                                             exec_report,
                                             f'Verify that {JavaApiFields.LeavesQty.value}, does not change')
        self.java_api_manager.compare_values({'TransExecSts is present': JavaApiFields.TransExecStatus.value},
                                             {'TransExecSts is present': exec_report}, 'Verify that order has Open status (step 3)', VerificationMethod.NOT_CONTAINS)
        # endregion

        # region step 4: Check 35 = Q message on Buy Gateway side
        dont_know_trade = FixDontKnowTrade(data_set=self.data_set)
        list_ignored_fields = ['SecurityDesc']
        dont_know_trade.set_default(last_venue_ord_id)
        dont_know_trade.change_parameters({'DKReason': 'E',
                                           'LastQty': qty,
                                           'LastPx': new_price,
                                           'OrderQtyData': {'OrderQty': qty},
                                           'Side': '1'})
        self.fix_verifier_bs.check_fix_message_fix_standard(dont_know_trade, ignored_fields=list_ignored_fields)

        # region step 4 part 2: Check that mip message has venueExecID field
        self._check_logs(venue_exec_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST")
        time.sleep(50)
        os.remove('temp.xml')
        self.ssh_client.close()
        self.db_manager.close_connection()

    def _check_logs(self, venue_exec_id):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command(
            f'egrep "gateway DontKnowTrade.*.VenueExecID=.{venue_exec_id}.*." QUOD.FIXBUYTH2TEST.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        with open('./logs.txt') as file:
            res = file.readlines()
        self.java_api_manager.compare_values({'VenueExecIDPresend': f'VenueExecID="{venue_exec_id}"'},
                                             {'VenueExecIDPresend': res[-1]},
                                             'Verify that VenueExecID presends in mip message to BE',
                                             VerificationMethod.CONTAINS)
        os.remove('./logs.txt')
