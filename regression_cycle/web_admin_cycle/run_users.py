import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.users.QAP_1640 import QAP_1640
from test_cases.web_admin.web_admin_test_cases.users.QAP_2256 import QAP_2256
from test_cases.web_admin.web_admin_test_cases.users.QAP_2257 import QAP_2257
from test_cases.web_admin.web_admin_test_cases.users.QAP_2259 import QAP_2259
from test_cases.web_admin.web_admin_test_cases.users.QAP_2405 import QAP_2405
from test_cases.web_admin.web_admin_test_cases.users.QAP_2451 import QAP_2451
from test_cases.web_admin.web_admin_test_cases.users.QAP_2578 import QAP_2578
from test_cases.web_admin.web_admin_test_cases.users.QAP_2863 import QAP_2863
from test_cases.web_admin.web_admin_test_cases.users.QAP_3100 import QAP_3100
from test_cases.web_admin.web_admin_test_cases.users.QAP_3145 import QAP_3145
from test_cases.web_admin.web_admin_test_cases.users.QAP_4186 import QAP_4186
from test_cases.web_admin.web_admin_test_cases.users.QAP_4239 import QAP_4239
from test_cases.web_admin.web_admin_test_cases.users.QAP_4329 import QAP_4329
from test_cases.web_admin.web_admin_test_cases.users.QAP_4855 import QAP_4855
from test_cases.web_admin.web_admin_test_cases.users.QAP_5842 import QAP_5842
from test_cases.web_admin.web_admin_test_cases.users.QAP_918 import QAP_918
from test_cases.web_admin.web_admin_test_cases.users.QAP_919 import QAP_919


class RunUsers:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Users", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Users")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()

            QAP_918(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_919(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_1640(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2256(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2257(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2259(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2405(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2451(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2578(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2863(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3100(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3145(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4186(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4239(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4329(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4855(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5842(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Users ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
