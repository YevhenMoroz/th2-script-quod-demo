import logging
import time
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixDontKnowTrade import FixDontKnowTrade
from test_framework.fix_wrappers.FixVerifier import FixVerifier
import xml.etree.ElementTree as ET
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.es_messages.NewOrderReplyOMS import NewOrderReplyOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T10575(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)

        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_pt_1_venue_1")  # MOClient_PARIS
        self.venue = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
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
        # region precondition
        tree = ET.parse(self.local_path)
        element_1 = ET.fromstring('<execution><duplicates>true</duplicates></execution>')
        es = tree.getroot().find('es')
        es.append(element_1)
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST")
        time.sleep(50)

        # endregion
        # region step 1: Send 35 = 8 message
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
        self.java_api_manager.compare_values(expected_result, ord_rep, 'Check order status')
        # endregion

        # region step 2: repeat 35=8 message:
        self.java_api_manager.send_message(self.nos)
        out = self.db_manager.execute_query(f"SELECT ordid FROM ordr WHERE clordid = '{cl_ord_id}'")
        value = True if len(out) == 1 else False
        self.java_api_manager.compare_values({'OnlyOneOrderPresent': True},
                                             {'OnlyOneOrderPresent': value},
                                             f'Verify that only order exists with following {JavaApiFields.ClOrdID.value} (step 2)')
        # endregion

        # region step 3: Partially Filled Unsolicited order
        self.exec_rep.set_default_trade(cl_ord_id)
        half_qty = str(float(ord_qty) / 2)
        self.exec_rep.update_fields_in_component('ExecutionReportBlock', {
            JavaApiFields.OrdQty.value: ord_qty,
            JavaApiFields.LastVenueOrdID.value: ord_venue_id,
            JavaApiFields.LastTradedQty.value: half_qty,
            JavaApiFields.LeavesQty.value: half_qty,
            JavaApiFields.CumQty.value: half_qty})
        filter_dict = {order_id: order_id}
        self.java_api_manager.send_message_and_receive_response(self.exec_rep, filter_dict)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
             JavaApiFields.LeavesQty.value: half_qty},
            execution_report,
            f'Verifying that order Partially filled and has properly {JavaApiFields.LeavesQty.value}')
        # endregion

        # region step 4: Resent the same execution report:
        self.java_api_manager.send_message(self.exec_rep)
        dont_know_trade = FixDontKnowTrade(data_set=self.data_set)
        list_ignored_fields = ['Side', 'LastPx'
                                       'LastQty', 'Instrument', 'OrderQtyData']
        dont_know_trade.set_default(ord_venue_id)
        dont_know_trade.change_parameters({'DKReason': 'Z'})
        self.fix_verifier_bs.check_fix_message_fix_standard(dont_know_trade)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart QUOD.ESBUYTH2TEST")
        time.sleep(50)
        self.ssh_client.close()
        self.db_manager.close_connection()
