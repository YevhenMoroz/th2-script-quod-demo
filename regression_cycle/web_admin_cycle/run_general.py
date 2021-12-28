import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.general.QAP_2450 import QAP_2450
from test_cases.web_admin.web_admin_test_cases.general.QAP_2454 import QAP_2454
from test_cases.web_admin.web_admin_test_cases.general.QAP_2509 import QAP_2509
from test_cases.web_admin.web_admin_test_cases.general.QAP_2516 import QAP_2516
from test_cases.web_admin.web_admin_test_cases.general.QAP_2544 import QAP_2544
from test_cases.web_admin.web_admin_test_cases.general.QAP_2616 import QAP_2616
from test_cases.web_admin.web_admin_test_cases.general.QAP_2624 import QAP_2624
from test_cases.web_admin.web_admin_test_cases.general.QAP_2631 import QAP_2631
from test_cases.web_admin.web_admin_test_cases.general.QAP_4104 import QAP_4104
from test_cases.web_admin.web_admin_test_cases.general.QAP_4865 import QAP_4865
from test_cases.web_admin.web_admin_test_cases.general.QAP_5840 import QAP_5840
from test_cases.web_admin.web_admin_test_cases.general.QAP_5967 import QAP_5967
from test_cases.web_admin.web_admin_test_cases.general.QAP_6152 import QAP_6152
from test_cases.web_admin.web_admin_test_cases.general.QAP_6182 import QAP_6182
from test_cases.web_admin.web_admin_test_cases.general.QAP_680 import QAP_680
from test_cases.web_admin.web_admin_test_cases.general.QAP_796 import QAP_796

from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.general.QAP_797 import QAP_797


class RunGeneral:
    def __init__(self, web_driver_container: WebDriverContainer,root_report_id):
        self.folder_name = 'WebAdmin'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()

            QAP_680(self.web_driver_container, self.second_lvl_id).run()
            # QAP_796(self.web_driver_container, self.second_lvl_id).run()
            # QAP_797(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2450(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2454(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2509(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2516(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2544(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2616(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2624(self.web_driver_container, self.second_lvl_id).run()
            # QAP_2631(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4104(self.web_driver_container, self.second_lvl_id).run()
            # QAP_4865(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5840(self.web_driver_container, self.second_lvl_id).run()
            # QAP_5967(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6152(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6182(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)