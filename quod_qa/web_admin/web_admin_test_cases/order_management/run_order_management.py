import time
import traceback
from datetime import timedelta

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_1567 import QAP_1567
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_1582 import QAP_1582
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2430 import QAP_2430
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2431 import QAP_2431
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2858 import QAP_2858
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2959 import QAP_2959
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2960 import QAP_2960
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2961 import QAP_2961
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2962 import QAP_2962
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2963 import QAP_2963
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2964 import QAP_2964
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2967 import QAP_2967
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2968 import QAP_2968
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2969 import QAP_2969
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_2970 import QAP_2970
from custom import basic_custom_actions as bca
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_4272 import QAP_4272
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_952 import QAP_952
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_958 import QAP_958
from quod_qa.web_admin.web_admin_test_cases.order_management.QAP_960 import QAP_960


class RunOrderManagement:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'web admin'
        self.first_lvl_id = bca.create_event(self.folder_name, root_report_id)
        self.second_lvl_id = bca.create_event(self.__class__.__name__, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()
            QAP_952(self.web_driver_container, self.second_lvl_id).run()
            QAP_958(self.web_driver_container, self.second_lvl_id).run()
            QAP_960(self.web_driver_container, self.second_lvl_id).run()
            QAP_1567(self.web_driver_container, self.second_lvl_id).run()
            QAP_1582(self.web_driver_container, self.second_lvl_id).run()
            QAP_2430(self.web_driver_container, self.second_lvl_id).run()
            QAP_2431(self.web_driver_container, self.second_lvl_id).run()
            QAP_2858(self.web_driver_container, self.second_lvl_id).run()
            QAP_2959(self.web_driver_container, self.second_lvl_id).run()
            QAP_2960(self.web_driver_container, self.second_lvl_id).run()
            QAP_2961(self.web_driver_container, self.second_lvl_id).run()
            QAP_2962(self.web_driver_container, self.second_lvl_id).run()
            QAP_2963(self.web_driver_container, self.second_lvl_id).run()
            QAP_2964(self.web_driver_container, self.second_lvl_id).run()
            QAP_2967(self.web_driver_container, self.second_lvl_id).run()
            QAP_2968(self.web_driver_container, self.second_lvl_id).run()
            QAP_2969(self.web_driver_container, self.second_lvl_id).run()
            QAP_2970(self.web_driver_container, self.second_lvl_id).run()
            QAP_4272(self.web_driver_container, self.second_lvl_id).run()

            end_time = time.monotonic()
            print("Run Order Management ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)


