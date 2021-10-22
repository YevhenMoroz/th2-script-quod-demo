import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.risk_limits.QAP_2455 import QAP_2455
from quod_qa.web_admin.web_admin_test_cases.risk_limits.QAP_4851 import QAP_4851
from quod_qa.web_admin.web_admin_test_cases.site.QAP_5364 import QAP_5364


class RunSite:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_5364(self.web_driver_container, self.second_lvl_id).run()
            end_time = time.monotonic()
            print("Run Site ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
