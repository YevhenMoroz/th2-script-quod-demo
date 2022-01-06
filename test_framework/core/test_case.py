from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from abc import ABC, abstractmethod


class TestCase(ABC):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        self.session_id = session_id
        self.report_id = report_id
        self.data_set = data_set
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    @abstractmethod
    def run_pre_conditions_and_steps(self):
        pass

    @abstractmethod
    def run_post_conditions(self):
        pass

    def execute(self):
        self.run_pre_conditions_and_steps()
        self.run_post_conditions()
