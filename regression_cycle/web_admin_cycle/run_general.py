import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.general.QAP_2450 import QAP_2450
from quod_qa.web_admin.web_admin_test_cases.general.QAP_2509 import QAP_2509
from quod_qa.web_admin.web_admin_test_cases.general.QAP_2544 import QAP_2544
from quod_qa.web_admin.web_admin_test_cases.general.QAP_2624 import QAP_2624
from quod_qa.web_admin.web_admin_test_cases.general.QAP_2631 import QAP_2631
from quod_qa.web_admin.web_admin_test_cases.general.QAP_796 import QAP_796

from custom import basic_custom_actions as bca
class RunGeneral:
    def __init__(self, web_driver_container: WebDriverContainer,root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()

            QAP_796(self.web_driver_container, self.second_lvl_id).run()
            QAP_2450(self.web_driver_container, self.second_lvl_id).run()
            QAP_2509(self.web_driver_container, self.second_lvl_id).run()
            QAP_2544(self.web_driver_container, self.second_lvl_id).run()
            QAP_2624(self.web_driver_container, self.second_lvl_id).run()
            QAP_2631(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)