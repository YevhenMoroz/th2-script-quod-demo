import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.general.QAP_2450 import QAP_2450
from test_cases.web_admin.web_admin_test_cases.general.QAP_2454 import QAP_2454
from test_cases.web_admin.web_admin_test_cases.general.QAP_2509 import QAP_2509
from test_cases.web_admin.web_admin_test_cases.general.QAP_2516 import QAP_2516
from test_cases.web_admin.web_admin_test_cases.general.QAP_2544 import QAP_2544
from test_cases.web_admin.web_admin_test_cases.general.QAP_2616 import QAP_2616
from test_cases.web_admin.web_admin_test_cases.general.QAP_2624 import QAP_2624
from test_cases.web_admin.web_admin_test_cases.general.QAP_2631 import QAP_2631
from test_cases.web_admin.web_admin_test_cases.general.QAP_2632 import QAP_2632
from test_cases.web_admin.web_admin_test_cases.general.QAP_2851 import QAP_2851
from test_cases.web_admin.web_admin_test_cases.general.QAP_3015 import QAP_3015
from test_cases.web_admin.web_admin_test_cases.general.QAP_4104 import QAP_4104
from test_cases.web_admin.web_admin_test_cases.general.QAP_4865 import QAP_4865
from test_cases.web_admin.web_admin_test_cases.general.QAP_5840 import QAP_5840
from test_cases.web_admin.web_admin_test_cases.general.QAP_5967 import QAP_5967
from test_cases.web_admin.web_admin_test_cases.general.QAP_6152 import QAP_6152
from test_cases.web_admin.web_admin_test_cases.general.QAP_6182 import QAP_6182
from test_cases.web_admin.web_admin_test_cases.general.QAP_796 import QAP_796
from test_cases.web_admin.web_admin_test_cases.general.QAP_797 import QAP_797
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunGeneral:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_General", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_General")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_796(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_797(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_2450(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2454(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2509(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2516(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2544(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2616(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2624(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2631(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2632(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_2851(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_3015(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4104(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4865(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5840(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5967(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6152(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6182(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
