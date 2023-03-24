from test_framework.mobile_android_core.utils.driver import AppiumDriver
from custom.verifier import Verifier
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from custom import basic_custom_actions as bca
from test_framework.mobile_android_core.utils.waits import Waits
import abc

class CommonTestCase:
    def __init__(self, driver: AppiumDriver, test_case_id, root_id, data_set: BaseDataSet = None,
                 environment: FullEnvironment = None):
        ## event creation
        self.appium_driver = driver
        self.test_id = bca.create_event(test_case_id, root_id)
        self.data_set = data_set
        self.environment = environment
        self.Waiter = Waits(self.appium_driver.appium_driver, 10)

    def run(self):
        self.__start_driver()
        self.test_context()
        self.__stop_driver()

    @abc.abstractmethod
    def test_context(self):
        raise NotImplementedError("Please implement this method!")

    def __start_driver(self):
        self.appium_driver.start_appium_service()

    def __stop_driver(self):
        self.appium_driver.stop_appium_service()

    ## verify methods

    def verify(self, event_name, expected_result, actual_result):
        verifier = Verifier(self.test_id)
        verifier.set_event_name(event_name)
        verifier.compare_values(event_name, str(expected_result), str(actual_result))
        verifier.verify()
