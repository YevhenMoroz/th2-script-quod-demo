import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_2455 import QAP_2455
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_4851 import QAP_4851
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5599 import QAP_5599
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5606 import QAP_5606
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5607 import QAP_5607
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_780 import QAP_780
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_783 import QAP_783


class RunRiskLimits:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_780(self.web_driver_container, self.second_lvl_id).run()
            QAP_783(self.web_driver_container, self.second_lvl_id).run()
            QAP_2455(self.web_driver_container, self.second_lvl_id).run()
            QAP_4851(self.web_driver_container, self.second_lvl_id).run()
            QAP_5599(self.web_driver_container, self.second_lvl_id).run()
            QAP_5606(self.web_driver_container, self.second_lvl_id).run()
            QAP_5607(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Risk Limits ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
