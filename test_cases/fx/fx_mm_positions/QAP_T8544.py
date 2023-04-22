from pathlib import Path
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.FixRequestForPositionsFX import FixRequestForPositionsFX
from test_framework.java_api_wrappers.fx.RequestForFXPositions import RequestForFXPositions

from custom import basic_custom_actions as bca


class QAP_T8544(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.position_request = RequestForFXPositions(data_set=self.data_set)
        self.act_java_api = Stubs.act_java_api
        self.request = FixRequestForPositionsFX()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # self.position_request.set_default_params()
        # # self.position_request.change_subject("CLIENT1")
        # self.java_api_manager.send_message(self.position_request)
        #
        self.request.set_default_params()
        response: list = self.java_api_manager.send_message_and_receive_response(self.request)
        print(response[0].get_parameters())
        self.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.request.unsubscribe()
        self.java_api_manager.send_message(self.request)
