import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest
from test_framework.java_api_wrappers.ors_messages.OrderSubmit import OrderSubmit
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7169(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client('client_co_1')
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.manual_cross = ManualOrderCrossRequest()
        self.submit_request = OrderSubmit()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.qty = '100'
        self.price = '10'
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set up configuration on BackEnd(precondition)
        self.ssh_client.send_command("/home/quod317/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(45)
        # endregion

        # region create CO  orders (precondition)
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        client_order_id = response[0].get_parameters()['ClOrdID']
        self.fix_message.change_parameters({'ClOrdID': basic_custom_actions.client_orderid(9), 'Side': '2'})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id_2 = response[0].get_parameters()['OrderID']
        client_order_id_2 = response[0].get_parameters()['ClOrdID']

        # region trade via manual cross CO orders (step 2)
        self.manual_cross.set_default(self.data_set, order_id, order_id_2, exec_qty=self.qty, exec_price=self.price)
        self.java_api_manager.send_message(self.manual_cross)
        # endregion

        # region check fix message (step 3)
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.fix_message.change_parameters({'ClOrdID': client_order_id, 'Side': '1'})
        execution_report.set_default_filled(self.fix_message)
        execution_report.remove_parameter('SecondaryOrderID').remove_parameter('SecondaryExecID'). \
            remove_parameter('SettlCurrency').remove_parameter('LastExecutionPolicy').change_parameters(
            {'VenueType': 'O', 'LastMkt': '*', 'TradeReportingIndicator': '0',
             'TrdSubType': '*', 'TrdType': '*', 'LastCapacity': '*'})
        list_of_ignored_fields = ['MiscFeesGrp', 'CommissionData', 'SecurityDesc']
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        execution_report.change_parameters({'ClOrdID': client_order_id_2, 'Side': '2'})
        self.fix_verifier.check_fix_message_fix_standard(execution_report,
                                                         ignored_fields=list_of_ignored_fields)
        # endregion

    @try_except
    def run_post_conditions(self):
        self.ssh_client.send_command("/home/quod317/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N")
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(45)
