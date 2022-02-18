import time
import traceback
from datetime import timedelta

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.positions.QAP_2165 import QAP_2165
from test_cases.web_admin.web_admin_test_cases.positions.QAP_2166 import QAP_2166
from test_cases.web_admin.web_admin_test_cases.positions.QAP_2167 import QAP_2167
from test_cases.web_admin.web_admin_test_cases.positions.QAP_2168 import QAP_2168


class RunPositions:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
# Пройти мануально
            QAP_2165(self.web_driver_container, self.second_lvl_id).run()
            QAP_2166(self.web_driver_container, self.second_lvl_id).run()
            QAP_2167(self.web_driver_container, self.second_lvl_id).run()
            QAP_2168(self.web_driver_container, self.second_lvl_id).run()
            end_time = time.monotonic()
            print("Run Positions ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
