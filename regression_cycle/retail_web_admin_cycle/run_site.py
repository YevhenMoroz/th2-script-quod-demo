import time
import traceback
from datetime import timedelta

from test_cases.web_admin.retail_web_admin_test_cases.site.QAP_T3585 import QAP_T3585
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunSite:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            #QAP_T3704(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3703(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3701(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3700(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3695(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3694(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3692(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3697(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3699(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3696(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3652(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3650(self.web_driver_container, self.second_lvl_id).run()
            QAP_T3585(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3584(self.web_driver_container, self.second_lvl_id).run()
            #QAP_T3577(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Site Retail ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
