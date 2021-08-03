import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_1740 import QAP_1740
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2182 import QAP_2182
from quod_qa.web_admin.web_admin_test_cases.client_accounts.QAP_2197 import QAP_2197
from quod_qa.web_admin.web_admin_test_cases.positions.QAP_2165 import QAP_2165
from quod_qa.web_admin.web_admin_test_cases.positions.QAP_2168 import QAP_2168

from custom import basic_custom_actions as bca


class RunClientsAccounts:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'web admin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_2182(self.web_driver_container, self.second_lvl_id).run()
            QAP_2197(self.web_driver_container, self.second_lvl_id).run()
            QAP_1740(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Client/Accounts ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
