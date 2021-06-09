import abc
from datetime import datetime

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from stubs import Stubs


class CommonTestCase:
    def __init__(self, web_driver_container: WebDriverContainer, test_case_id):
        self.web_driver_container = web_driver_container
        self.report_id = bca.create_event(f'{Stubs.custom_config["web_admin_login"]} tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
        self.test_case_id = bca.create_event(test_case_id, self.report_id)

    # TODO: resolve issue with missing error message in the except block
    def run(self):
        # try:
            self.__start_driver()
            self.test_context()
        # except Exception as e:
            # print("An error was occurred during the test case execution!\n" + str(e))
        # finally:
            self.__stop_driver()

    @abc.abstractmethod
    def test_context(self):
        raise NotImplementedError("Please implement this method!")

    def __start_driver(self):
        self.web_driver_container.start_driver()

    def __stop_driver(self):
        self.web_driver_container.stop_driver()

    def verify(self, event_name, expected_result, actual_result):
        verifier = Verifier(self.test_case_id)
        verifier.set_event_name(event_name)
        verifier.compare_values(event_name, str(expected_result), str(actual_result))
        verifier.verify()
