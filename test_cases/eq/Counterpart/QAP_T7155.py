import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7155(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters({'Account': self.client})
        self.fix_message2.change_parameters({'Account': self.client})
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.manual_cross = ManualOrderCrossRequest()
        self.client_id = self.fix_message.get_parameter('ClOrdID')
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Setup ORS
        tree = ET.parse(self.local_path)
        root = tree.getroot()
        root.find("ors/BackToFront/FIXReportOrdrParties").text = "false"
        root.find("ors/BackToFront/EnrichFIXExecReportParties").text = "false"
        root.find("ors/counterpartEnrichment/ManualOrderCross").text = "false"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        # endregion
        # region send  first order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # region Declaration
        # region send  second order
        self.fix_message2.change_parameter("Side", "2")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message2)
        order_id_2 = response[0].get_parameters()['OrderID']
        # endregion
        # region manual cross orders
        self.manual_cross.set_default(self.data_set, order_id, order_id_2, exec_qty=self.qty, exec_price=self.price)
        self.java_api_manager.send_message(self.manual_cross)
        # endregion
        # region send exec report
        execution_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        execution_report1.change_parameters({'Parties': '#'})
        self.fix_verifier.check_fix_message_fix_standard(execution_report1,
                                                         ignored_fields=['GatingRuleCondName',
                                                                         'GatingRuleName', 'TrdSubType',
                                                                         'SettlCurrency', 'LastExecutionPolicy',
                                                                         'TrdType', 'LastCapacity',
                                                                         'SecondaryOrderID', 'LastMkt',
                                                                         'VenueType'])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(60)
        os.remove("temp.xml")
