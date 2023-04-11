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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, TimeInForces
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
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


class QAP_T8910(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.bs_connectivity = self.fix_env.buy_side
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.order_submit = OrderSubmitOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition-step 1: Create DMA order and check that it`s has properly status
        holiday_date = (datetime.datetime.now() + datetime.timedelta(1)).strftime('%Y%m%d')
        today_date = (datetime.datetime.now()).strftime('%Y-%b-%d')
        self.order_submit.set_default_dma_limit()
        route = self.data_set.get_route_id_by_name("route_1")
        route_params = {JavaApiFields.RouteBlock.value: [{JavaApiFields.RouteID.value: route}]}
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.RouteList.value: route_params,
                                                      JavaApiFields.TimeInForce.value: TimeInForces.DAY.value,
                                                      })
        price = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][JavaApiFields.Price.value]
        try:
            self._set_up_holiday(holiday_date)
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(price))
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value). \
                get_parameters()[JavaApiFields.OrdReplyBlock.value]
            expected_message = f'11662 Current day ({today_date}) is not a trading day / Current day ({today_date}) is not a trading day'
            self.java_api_manager.compare_values(
                {JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value,
                 JavaApiFields.FreeNotes: expected_message},
                order_reply, f'Verifying that order created and has properly {JavaApiFields.EffectiveDate.value}')

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self._remove_holiday()
            self.db_manager.close_connection()

    def _set_up_holiday(self, holiday_date):
        self.db_manager.execute_query(f"INSERT INTO holidaycalendar (holidayid, holidaydate,holidaydescription, alive, "
                                      f"tradingallowed) VALUES ('3', {holiday_date}, 'gvnch', 'Y','N')")
        day_today = _which_is_day_today()
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = '{day_today}'
                                                    WHERE venueid = 'PARIS'""")
        self.ssh_client.send_command("qrestart all")
        time.sleep(180)

    def _remove_holiday(self):
        self.db_manager.execute_query(f"DELETE FROM holidaycalendar WHERE holidayid = '3'")
        self.db_manager.execute_query(f"""UPDATE  venue SET  weekendday = null
                                                            WHERE venueid = 'PARIS'""")
        self.ssh_client.close()

    def _convert_mounts_to_world(self, date: str):

        return date.replace('')
