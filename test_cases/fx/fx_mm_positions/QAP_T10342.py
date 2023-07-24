from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleTaker import FixMessageNewOrderSingleTaker
from test_framework.fix_wrappers.forex.FixMessageOrderCancelRequestFX import FixMessageOrderCancelRequestFX
from test_framework.fix_wrappers.forex.FixMessagePositionReportFX import FixMessagePositionReportFX
from test_framework.fix_wrappers.forex.FixMessageRequestForPositionsFX import FixMessageRequestForPositionsFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixPositionMassCancelRequestFX import FixPositionMassCancelRequestFX
from test_framework.positon_verifier_fx import PositionVerifier


class QAP_T10342(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.pks_connectivity = self.environment.get_list_fix_environment()[0].sell_side_pks
        self.taker_connectivity = self.environment.get_list_fix_environment()[0].buy_side_esp
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager_pks = FixManager(self.pks_connectivity, self.test_id)
        self.fix_manager_taker = FixManager(self.taker_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.pks_connectivity, self.test_id)
        self.request_for_position = FixMessageRequestForPositionsFX()
        self.position_verifier = PositionVerifier(self.test_id)
        self.position_report = FixMessagePositionReportFX()
        self.cancel_request = FixPositionMassCancelRequestFX()
        self.new_order_singe = FixMessageNewOrderSingleTaker(data_set=self.data_set)
        self.order_cancel = FixMessageOrderCancelRequestFX()

        self.client = self.data_set.get_client_by_name("client_5")
        self.account = self.data_set.get_account_by_name("account_5")
        self.order_qty = "10000000"
        self.base_qty = "0"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Clear positions before test
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
        # endregion
        # region Step 1
        self.new_order_singe.set_default_care()
        self.new_order_singe.change_parameter("OrderQty", self.order_qty)
        self.new_order_singe.change_parameter("Account", self.client)
        exec_report: list = self.fix_manager_taker.send_message_and_receive_response(self.new_order_singe)
        order_id = exec_report[0].get_parameters()["OrderID"]
        # endregion

        # region Step 2
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        response: list = self.fix_manager_pks.send_message_and_receive_response(self.request_for_position, self.test_id)
        self.position_verifier.check_working_positions(response, self.order_qty)
        self.position_report.set_params_from_reqeust(self.request_for_position)
        self.position_report.change_parameter("LastPositUpdateEventID", order_id)
        self.fix_verifier.check_fix_message(self.position_report)
        self.request_for_position.set_unsubscribe()
        self.fix_manager_pks.send_message(self.request_for_position)
        # endregion

        # region Step 3
        self.order_cancel.set_params_for_order(self.new_order_singe)
        self.fix_manager_taker.send_message(self.order_cancel)
        # endregion

        # region Step 4
        self.request_for_position.set_default()
        self.request_for_position.change_parameter("Account", self.client)
        response: list = self.fix_manager_pks.send_message_and_receive_response(self.request_for_position, self.test_id)
        self.position_verifier.check_working_positions(response, self.base_qty)
        self.position_report.set_params_from_reqeust(self.request_for_position)
        self.position_report.change_parameter("LastPositEventType", 4)
        self.fix_verifier.check_fix_message(self.position_report)
        self.request_for_position.set_unsubscribe()
        self.fix_manager_pks.send_message(self.request_for_position)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.cancel_request.set_params(self.account)
        self.java_api_manager.send_message(self.cancel_request)
        self.sleep(5)
