import time
import traceback
from datetime import timedelta

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer

from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.client_accounts.QAP_T3593 import QAP_T3593


class RunClientsAccounts:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:

            start_time = time.monotonic()
            # QAP_T3770(self.web_driver_container, self.second_lvl_id).run()
            # QAP_T3733(self.web_driver_container, self.second_lvl_id).run()
            # QAP_T3724(self.web_driver_container, self.second_lvl_id).run()
            # QAP_T3762(self.web_driver_container, self.second_lvl_id).run()
            # QAP_T3753(self.web_driver_container, self.second_lvl_id).run()
            QAP_T3593(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Client/Accounts Retail ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
