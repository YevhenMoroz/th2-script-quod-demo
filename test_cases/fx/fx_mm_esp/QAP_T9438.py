from datetime import datetime, timedelta
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.MarketDataRequestFX import MarketDataRequestFX
from test_framework.java_api_wrappers.fx.MarketDataSnapshotFX import MarketDataSnapshotFX


class QAP_T9438(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.md_request = MarketDataRequestFX()
        self.md_snapshot = MarketDataSnapshotFX()
        self.verifier = Verifier(self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.md_request.set_default_params_sub()
        response: list = self.java_api_manager.send_message_and_receive_response(self.md_request)
        time_stamps = response[-1].get_timestamps()
        now = (datetime.now() - timedelta(hours=5))
        expected_timestamp = now.isoformat().rsplit("T")[0]
        actual_timestamp_1 = time_stamps[1].rsplit("T")[0]
        actual_timestamp_2 = time_stamps[2].rsplit("T")[0]
        self.verifier.set_event_name("Compare timestamps")
        self.verifier.compare_values("Compare OrigVenueID", "HSBC", time_stamps[0])
        self.verifier.compare_values("Compare OrigMDTime", expected_timestamp, actual_timestamp_1)
        self.verifier.compare_values("Compare OrigMDArrivalTime", expected_timestamp, actual_timestamp_2)
        self.verifier.verify()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.unsubscribe()
        self.java_api_manager.send_message(self.md_request)
