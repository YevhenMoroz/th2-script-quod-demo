from test_framework.mobile_android_core.utils.driver import AppiumDriver
from custom.verifier import Verifier
from custom import basic_custom_actions as bca
import abc

class CommonTestCase:
    def __init__(self,driver:AppiumDriver,test_case_id , root_id ):
        ## cоздание ивента
        self.appium_driver = driver
        self.test_case_id = bca.create_event(test_case_id, root_id)


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
        verifier = Verifier(self.test_case_id)
        verifier.set_event_name(event_name)
        verifier.compare_values(event_name, str(expected_result), str(actual_result))
        verifier.verify()

    # def verify_arrays_of_data_objects(self, page_name, event_name, expected_result, actual_result):
    #     verifier = Verifier(self.test_case_id)
    #     verifier.set_event_name(page_name)
    #     for item in range(len(event_name)):
    #         verifier.compare_values(event_name[item], expected_result[item], actual_result[item])
    #     verifier.verify()