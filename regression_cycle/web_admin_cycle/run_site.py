import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.site.QAP_5364 import QAP_5364
from test_cases.web_admin.web_admin_test_cases.site.QAP_5578 import QAP_5578
from test_cases.web_admin.web_admin_test_cases.site.QAP_5579 import QAP_5579
from test_cases.web_admin.web_admin_test_cases.site.QAP_5580 import QAP_5580
from test_cases.web_admin.web_admin_test_cases.site.QAP_5583 import QAP_5583
from test_cases.web_admin.web_admin_test_cases.site.QAP_6346 import QAP_6346


class RunSite:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Site", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Site")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_5364(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5578(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5579(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5580(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5583(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6346(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Site ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
