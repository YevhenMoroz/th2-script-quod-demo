import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3149 import QAP_T3149
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3150 import QAP_T3150
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3151 import QAP_T3151
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3175 import QAP_T3175
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3176 import QAP_T3176
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3177 import QAP_T3177
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3197 import QAP_T3197
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3198 import QAP_T3198
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T3265 import QAP_T3265
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T8138 import QAP_T8138
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T8139 import QAP_T8139
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T8140 import QAP_T8140
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T8149 import QAP_T8149
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T8150 import QAP_T8150
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T8151 import QAP_T8151
from test_cases.web_admin.web_admin_test_cases.price_cleansing.QAP_T9422 import QAP_T9422

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunPriceCleansing:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Price_Cleansing", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Price_Cleansing")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()

            QAP_T3149(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3150(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3151(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3175(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3176(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3177(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3197(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3198(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3265(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8138(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8139(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8140(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8149(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8150(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8151(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T9422(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Price Cleansing ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
