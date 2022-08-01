import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_2455 import QAP_2455
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_4851 import QAP_4851
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_4966 import QAP_4966
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_4969 import QAP_4969
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_4975 import QAP_4975
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5018 import QAP_5018
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5019 import QAP_5019
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5599 import QAP_5599
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5606 import QAP_5606
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_5607 import QAP_5607
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_6382 import QAP_6382
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_6384 import QAP_6384
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_7108 import QAP_7108
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_7371 import QAP_7371
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_7528 import QAP_7528
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_7966 import QAP_7966
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_780 import QAP_780
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_783 import QAP_783
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca


class RunRiskLimits:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Risk_Limits", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Risk_Limits")  # look at xml (component name="web_admin_general")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_780(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_783(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_2455(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4851(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4966(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4969(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_4975(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5018(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5019(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5599(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5606(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_5607(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6382(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6384(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_7108(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_7371(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_7528(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_7966(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Risk Limits ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
