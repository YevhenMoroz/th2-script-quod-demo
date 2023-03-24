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

    def compare_values(self, test_id, expected_value: list, actual_value: list, event_name: str = "Compare values",
                       ver_method: VerificationMethod = VerificationMethod.EQUALS):
        verifier = Verifier(test_id)
        verifier.set_event_name(event_name)

        for i in range(len(expected_value)):
            verifier.compare_values(f"Compare value {i + 1}", expected_value[i], actual_value[i],
                                    verification_method=ver_method)
        verifier.verify()
