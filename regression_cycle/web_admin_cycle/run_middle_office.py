import time
import traceback
from datetime import timedelta

from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_2564 import QAP_2564
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_3148 import QAP_3148
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_3152 import QAP_3152
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_3219 import QAP_3219
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_3222 import QAP_3222
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_3223 import QAP_3223
from quod_qa.web_admin.web_admin_test_cases.middle_office.QAP_4858 import QAP_4858


class RunMiddleOffice:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_2564(self.web_driver_container, self.second_lvl_id).run()
            QAP_3148(self.web_driver_container, self.second_lvl_id).run()
            QAP_3152(self.web_driver_container, self.second_lvl_id).run()
            QAP_3219(self.web_driver_container, self.second_lvl_id).run()
            QAP_3222(self.web_driver_container, self.second_lvl_id).run()
            QAP_3223(self.web_driver_container, self.second_lvl_id).run()
            QAP_4858(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Middle Office ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
