import datetime
import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7185(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.fix_new_ord_single = FixMessageNewOrderSingleOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition-step 1: Create DMA order and check that it`s has properly status
        # part 1: Set up precondition
        list_holiday_dates = [(datetime.datetime.now() + datetime.timedelta(days=8)).strftime('%Y-%m-%d'),
                              (datetime.datetime.now() + datetime.timedelta(days=9)).strftime('%Y-%m-%d')]
        list_expected_expire_times = [
            (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%dT15:23:23'),
            (datetime.datetime.now() + datetime.timedelta(days=9)).strftime('%Y-%m-%dT15:23:23')]
        for holiday_date in list_holiday_dates:
            expire_time = holiday_date + 'T15:23:23'
            expected_expire_time = list_expected_expire_times[list_holiday_dates.index(holiday_date)]
            self.fix_new_ord_single.set_default_dma_limit()
            price = self.fix_new_ord_single.get_parameters()['Price']
            self.fix_new_ord_single.change_parameters({"TimeInForce": '6', 'ExpireTime': expire_time})
            datetime.datetime.fromisoformat(holiday_date)
            if holiday_date == list_holiday_dates[0]:
                holiday_date = datetime.datetime.fromisoformat(holiday_date).strftime('%Y%m%d')
                self._set_up_holiday(holiday_date)
            # end_of_part
            # endregion

            # region step 1 : Create DMA order via FIX
            try:
                new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                    self.fix_env.buy_side, self.venue_client_name, self.mic, float(price))
                self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_new_ord_single)
            except Exception as e:
                logger.error(f'{e}', exc_info=True)
            finally:
                time.sleep(1)
                self.rule_manager.remove_rule(new_order_single_rule)

            # endregion

            # region step 2: Check expire time of order
            exec_rep = self.fix_manager.get_last_message("ExecutionReport", "'ExecType': '0'").get_parameters()
            self.fix_manager.compare_values({'ExpireTime': expected_expire_time},
                                            exec_rep, 'Verify that execution report has correct ExpireDate (step 2)')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self._remove_holiday()
        self.db_manager.close_connection()
        self.ssh_client.close()

    def _set_up_holiday(self, holiday_date):
        self.db_manager.execute_query(f"INSERT INTO holidaycalendar (holidayid, holidaydate,holidaydescription, alive, "
                                      f"tradingallowed) VALUES ('3', {holiday_date}, 'gvnch', 'Y','N')")

        self.ssh_client.send_command("qrestart QUOD.AQS QUOD.ORS QUOD.ESBUYTH2TEST")
        time.sleep(120)

    def _remove_holiday(self):
        self.db_manager.execute_query(f"DELETE FROM holidaycalendar WHERE holidayid = '3'")
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = null
                                                            WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart QUOD.AQS QUOD.ORS QUOD.ESBUYTH2TEST")
        time.sleep(120)
