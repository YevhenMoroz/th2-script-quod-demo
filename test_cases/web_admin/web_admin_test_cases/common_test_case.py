import abc

from pathlib import Path
from test_framework.core.try_exept_decorator import try_except

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommonTestCase:
    def __init__(self, web_driver_container: WebDriverContainer, test_case_id, root_id, data_set: BaseDataSet = None,
                 environment: FullEnvironment = None):
        self.web_driver_container = web_driver_container
        self.test_id = bca.create_event(test_case_id, root_id)
        self.data_set = data_set
        self.environment = environment

    @try_except(test_id=Path(__file__).name[:-3])
    def run(self):
        self.__start_driver()
        self.test_context()
        self.__stop_driver()

    @abc.abstractmethod
    def test_context(self):
        raise NotImplementedError("Please implement this method!")

    def __start_driver(self):
        self.web_driver_container.start_driver()

    def __stop_driver(self):
        self.web_driver_container.stop_driver()

    def verify(self, event_name, expected_result, actual_result):
        verifier = Verifier(self.test_id)
        verifier.set_event_name(event_name)
        verifier.compare_values(event_name, str(expected_result), str(actual_result))
        verifier.verify()

    def verify_arrays_of_data_objects(self, page_name, event_name, expected_result, actual_result):
        verifier = Verifier(self.test_id)
        verifier.set_event_name(page_name)
        for item in range(len(event_name)):
            verifier.compare_values(event_name[item], expected_result[item], actual_result[item])
        verifier.verify()
