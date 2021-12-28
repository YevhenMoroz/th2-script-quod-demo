from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.base_window import decorator_try_except


class TestCase:
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        self.session_id = session_id
        self.report_id = report_id
        self.data_set = data_set
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

    def pre_conditions_and_run(self):
        raise Exception("You need to override pre_conditions_and_run method in child class test")

    def post_conditions(self):
        raise Exception("You need to override post_conditions method in child class test")

    def execute(self):
        self.pre_conditions_and_run()
        self.post_conditions()
