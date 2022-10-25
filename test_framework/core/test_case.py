import time

from custom.verifier import Verifier, VerificationMethod
from test_framework.data_sets.base_data_set import BaseDataSet
from abc import ABC, abstractmethod
from test_framework.environments.full_environment import FullEnvironment


class TestCase(ABC):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        self.session_id = session_id
        self.report_id = report_id
        self.data_set = data_set
        self.environment = environment
        self.verifier = Verifier()

    @abstractmethod
    def run_pre_conditions_and_steps(self):
        pass

    def run_post_conditions(self):
        pass

    def execute(self):
        self.run_pre_conditions_and_steps()
        self.run_post_conditions()

    def sleep(self, duration: int):
        time.sleep(duration)

    def compare_values(self, expected_value: str, actual_value: str, event_name: str = "Compare values",
                       ver_method: VerificationMethod = VerificationMethod.EQUALS, value_name: str = "Value"):
        self.verifier.set_event_name(event_name)
        self.verifier.compare_values(value_name, expected_value, actual_value, ver_method)
        self.verifier.verify()