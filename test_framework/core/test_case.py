from test_framework.data_sets.base_data_set import BaseDataSet


class TestCase:
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        self.session_id = session_id
        self.report_id = report_id
        self.data_set = data_set

    def pre_conditions_and_run(self):
        raise Exception("You need to override pre_conditions_and_run method in child class test")

    def post_conditions(self):
        raise Exception("You need to override post_conditions method in child class test")

    def execute(self):
        self.pre_conditions_and_run()
        self.post_conditions()
