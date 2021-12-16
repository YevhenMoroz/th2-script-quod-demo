import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_2564 import QAP_2564
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3148 import QAP_3148
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3152 import QAP_3152
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3219 import QAP_3219
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3222 import QAP_3222
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3223 import QAP_3223
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3225 import QAP_3225
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3235 import QAP_3235
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3236 import QAP_3236
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3237 import QAP_3237
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3238 import QAP_3238
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3240 import QAP_3240
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3603 import QAP_3603
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_3605 import QAP_3605
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_4152 import QAP_4152
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_4858 import QAP_4858
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_5448 import QAP_5448
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_5665 import QAP_5665
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_5666 import QAP_5666


class RunMiddleOffice:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_2564(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3148(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3152(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3219(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3222(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3223(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3225(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3235(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3236(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3237(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3238(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3240(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3603(self.web_driver_container, self.second_lvl_id).run()
            # QAP_3605(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4152(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4858(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5448(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5665(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5666(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Middle Office ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
