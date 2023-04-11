import datetime
import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


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


def _get_fix_message(parameter: dict, response):
    for i in range(len(response)):
        for j in parameter.keys():
            if response[i].get_parameters()[j] == parameter[j]:
                return response[i].get_parameters()


class QAP_T8909(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.fix_new_ord_single = FixMessageNewOrderSingleOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition-step 1: Create DMA order and check that it`s has properly status
        # part 1: Set up precondition
        holiday_date = (datetime.datetime.now() + datetime.timedelta(1)).strftime('%Y%m%d')
        expected_effective_date = (datetime.datetime.now() + datetime.timedelta(2)).strftime('%Y%m%d')
        self.fix_new_ord_single.set_default_care_limit(account='client_pt_1')
        cl_ord_id = self.fix_new_ord_single.get_parameters()[JavaApiFields.ClOrdID.value]
        self._set_up_holiday(holiday_date)
        # end_of_part

        # part 2 : Create CO order via FIX
        responses = self.fix_manager.send_message_and_receive_response(self.fix_new_ord_single)
        expected_values = {'ExecType': '0'}
        response = _get_fix_message({'ExecType': '0'}, responses)
        self.fix_manager.compare_values(
            expected_values,
            response, f'Verifying that order created (step 1)')
        effective_date_of_order = self._get_effective_date(cl_ord_id)
        self.fix_manager.compare_values(
            {JavaApiFields.EffectiveDate.value: expected_effective_date},
            {JavaApiFields.EffectiveDate.value: effective_date_of_order},
            f'Verifying that order has properly effective date (step 1)')
        # end_of_part
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self._remove_holiday()
        self.db_manager.close_connection()

    def _set_up_holiday(self, holiday_date):
        self.db_manager.execute_query(f"INSERT INTO holidaycalendar (holidayid, holidaydate,holidaydescription, alive, "
                                      f"tradingallowed) VALUES ('3', {holiday_date}, 'gvnch', 'Y','N')")
        day_today = _which_is_day_today()
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = '{day_today}'
                                                    WHERE venueid = 'PARIS'""")
        tree = ET.parse(self.local_path)
        delay_DAY = tree.getroot().find("ors/delayDayOrders")
        delay_DAY.text = 'true'
        tree.write("temp.xml")
        self.ssh_client.send_command('~/quod/script/site_scripts/change_permission_script')
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(200)

    def _remove_holiday(self):
        self.db_manager.execute_query(f"DELETE FROM holidaycalendar WHERE holidayid = '3'")
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = null
                                                            WHERE venueid = 'PARIS'""")
        self.ssh_client.put_file(self.remote_path, self.local_path)
        os.remove("temp.xml")
        self.ssh_client.send_command("qrestart all")
        time.sleep(200)
        self.ssh_client.close()

    def _get_effective_date(self, cl_ord_id):
        result = self.db_manager.execute_query(f"SELECT effectivedate FROM ordr WHERE clordid = {cl_ord_id}'")
        print(result)
        print(result[0][0])
        return result[0][0]
