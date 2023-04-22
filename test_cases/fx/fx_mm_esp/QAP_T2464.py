import time
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiOrderVelocityMessages import RestApiOrderVelocityMessages


class QAP_T2464(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_esp_connectivity = self.environment.get_list_fix_environment()[0].sell_side_esp
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_subscribe = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.velocity_rule = RestApiOrderVelocityMessages()
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.execution_report = FixMessageExecutionReportFX()
        self.execution_report_rej = FixMessageExecutionReportFX()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_esp_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_esp_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.qty_for_reject = "1000000"
        self.rest_message_params = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.velocity_rule.set_default_params().change_params({"accountGroupID": self.client,
                                                               "maxCumOrdQty": self.qty_for_reject}).create_limit()
        self.rest_manager.send_post_request(self.velocity_rule)
        self.sleep(3)

        self.velocity_rule.find_all_limits()
        self.rest_message_params = self.rest_manager.parse_create_response(
            self.rest_manager.send_get_request(self.velocity_rule))
        self.rest_message_params = self.rest_message_params["OrderVelocityLimitResponse"][0]
        limit_id = self.rest_message_params["orderVelocityLimitID"]
        time.sleep(5)
        # endregion
        # region Step 2
        self.fix_subscribe.set_md_req_parameters_maker().change_parameters({"SenderSubID": self.client})
        response = self.fix_manager_gtw.send_message_and_receive_response(self.fix_subscribe, self.test_id)
        self.fix_md_snapshot.set_params_for_md_response(self.fix_subscribe, response=response[0])
        self.fix_verifier.check_fix_message(fix_message=self.fix_md_snapshot)
        self.new_order_single.set_default().change_parameter("OrderQty", "500000")
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single,
                                                               response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
        # region Step 3
        self.new_order_single.set_default().change_parameter("OrderQty", self.qty_for_reject)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        reject = Status.Reject
        self.execution_report_rej.set_params_from_new_order_single(self.new_order_single, status=reject,
                                                                   response=response[-1])
        text = f"17568 Accumulated quantity of order creation/modification reached " \
               f"the limit {self.qty_for_reject} of 'OrderVelocityLimit' {limit_id}"
        self.execution_report_rej.change_parameter("Text", text)
        self.execution_report_rej.add_tag({"OrdRejReason": "99"})
        self.execution_report_rej.remove_parameters(["LastMkt", "ExecRestatementReason", "SettlType", "SettlCurrency"])
        self.fix_verifier.check_fix_message(self.execution_report_rej)
        # endregion
        # region Step 4
        self.sleep(30)
        self.new_order_single.set_default().change_parameter("OrderQty", "500000")
        response = self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single,
                                                               response=response[-1])
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.fix_subscribe.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.fix_subscribe, "Unsubscribe")
        self.velocity_rule.clear_message_params().set_params(self.rest_message_params).delete_limit()
        self.rest_manager.send_post_request(self.velocity_rule)
        self.sleep(2)
