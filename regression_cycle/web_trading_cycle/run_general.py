import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


#TODO: rename this file in future raleted to component
from test_cases.web_trading.test_cases.pages.login.QAP_test import QAP_test


class RunGeneral:
    def __init__(self, web_driver_container: WebDriverContainer,root_report_id):
        self.folder_name = 'WebTrading'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()

            QAP_test(self.web_driver_container, self.second_lvl_id).run() ## e.g. test, after you must change,rename or delete this


            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
