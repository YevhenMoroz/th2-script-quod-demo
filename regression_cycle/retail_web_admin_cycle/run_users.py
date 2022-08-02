import time
import traceback
from datetime import timedelta

from test_cases.web_admin.retail_web_admin_test_cases.users.QAP_T3631 import QAP_T3631

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca



class RunUsers:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            #QAP_T3763(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3655(self.web_driver_container, self.second_lvl_id).run()
            QAP_T3631(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3609(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Users ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
