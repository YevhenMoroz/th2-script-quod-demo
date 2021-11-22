import time
import traceback
from datetime import timedelta

from test_cases.web_admin.retail_web_admin_test_cases.risk_limits.QAP_4279 import QAP_4279
from test_cases.web_admin.retail_web_admin_test_cases.risk_limits.QAP_4319 import QAP_4319
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunRiskLimits:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            #QAP_4279(self.web_driver_container, self.second_lvl_id).run()
            QAP_4319(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Risk Limits retail ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
