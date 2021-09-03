import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1731 import QAP_1731
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1732 import QAP_1732
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_1733 import QAP_1733
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2302 import QAP_2302
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_2905 import QAP_2905
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_758 import QAP_758
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_759 import QAP_759
from quod_qa.web_admin.web_admin_test_cases.reference_data.QAP_760 import QAP_760


class ReferenceData:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_758(self.web_driver_container, self.second_lvl_id).run()
            QAP_759(self.web_driver_container, self.second_lvl_id).run()
            QAP_760(self.web_driver_container, self.second_lvl_id).run()
            QAP_1731(self.web_driver_container, self.second_lvl_id).run()
            QAP_1732(self.web_driver_container, self.second_lvl_id).run()
            QAP_1733(self.web_driver_container, self.second_lvl_id).run()
            QAP_2302(self.web_driver_container, self.second_lvl_id).run()
            QAP_2905(self.web_driver_container, self.second_lvl_id).run()
            end_time = time.monotonic()
            print("Reference data ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
