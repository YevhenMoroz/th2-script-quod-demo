import logging
import os
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, \
    OrderReplyConst, TimeInForces
import xml.etree.ElementTree as ET
from datetime import timedelta, date
import time
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


def _which_is_day_today():
    if 'Sat' in str(time.asctime(time.localtime())):
        return 6
    elif 'Sun' in str(time.asctime(time.localtime())):
        return 0
    elif 'Mon' in str(time.asctime(time.localtime())):
        return 1
    elif 'Tue' in str(time.asctime(time.localtime())):
        return 2
    elif 'Wed' in str(time.asctime(time.localtime())):
        return 3
    elif 'Thu' in str(time.asctime(time.localtime())):
        return 4
    elif 'Fri' in str(time.asctime(time.localtime())):
        return 5


class QAP_T10685(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client('client_pt_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.expire_effective_date = str(date.today() + timedelta(days=1)).replace('-', '')
        self.today = str(date.today()).replace('-', '')
        self.qty = '300'
        self.price = '10'
        self.day = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition:
        # part 1: make changes for venue
        self.day = _which_is_day_today()
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = '{self.day}'
                                            WHERE venueid = 'PARIS'""")
        # end_of_part

        # part 2 make changes in ORS
        tree = ET.parse(self.local_path)
        delay_GTC = tree.getroot().find("ors/delayGTCOrders")
        delay_GTD = tree.getroot().find("ors/delayGTDOrders")
        delay_GTD.text = 'true'
        delay_GTC.text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(250)
        # end_of_part

        # endregion:

        # region step 1 - 2: create DMA  orders with GTC and GTD tif
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.client_venue, self.mic, float(self.price))
            self.submit_request.set_default_dma_limit()
            route_params = {JavaApiFields.RouteBlock.value: [{JavaApiFields.RouteID.value: self.data_set.get_route_id_by_name("route_1")}]}
            self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                JavaApiFields.OrdQty.value: self.qty,
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.Price.value: self.price,
                JavaApiFields.RouteList.value: route_params,
                JavaApiFields.TimeInForce.value: TimeInForces.GTC.value
            })
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                 JavaApiFields.EffectiveDate.value: self.expire_effective_date},
                ord_reply,
                'Verifying that DMA order created and has properly values (step 1)')

            self.submit_request.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                JavaApiFields.ClOrdID.value: basic_custom_actions.client_orderid(9),
                JavaApiFields.TimeInForce.value: TimeInForces.GTD.value,
                JavaApiFields.ExpireDate.value: self.expire_effective_date
            })
            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_REJ.value,
                 JavaApiFields.EffectiveDate.value: self.today},
                ord_reply,
                'Verifying that DMA order created and has properly values (step 2)')


        finally:
            self.rule_manager.remove_rule(new_order_single)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = null
                                                    WHERE venueid = 'PARIS'""")
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart all")
        time.sleep(250)
        os.remove("temp.xml")
        self.ssh_client.close()
