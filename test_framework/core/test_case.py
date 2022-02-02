from test_framework.core.environment import Environment
from test_framework.data_sets.base_data_set import BaseDataSet
from abc import ABC, abstractmethod


class TestCase(ABC):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: Environment = None):
        self.session_id = session_id
        self.report_id = report_id
        self.data_set = data_set
        self.environment = environment

    @abstractmethod
    def run_pre_conditions_and_steps(self):
        pass

    def run_post_conditions(self):
        pass

    def execute(self):
        self.run_pre_conditions_and_steps()
        self.run_post_conditions()
