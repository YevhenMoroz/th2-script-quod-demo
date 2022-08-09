import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.others.QAP_T3973 import QAP_T3973
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3972 import QAP_T3972
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3970 import QAP_T3970
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3966 import QAP_T3966
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3889 import QAP_T3889
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3888 import QAP_T3888
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3834 import QAP_T3834
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3833 import QAP_T3833
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3824 import QAP_T3824
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3678 import QAP_T3678
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3677 import QAP_T3677
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3573 import QAP_T3573
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3545 import QAP_T3545
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3476 import QAP_T3476
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4039 import QAP_T4039
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4038 import QAP_T4038
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4037 import QAP_T4037
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4036 import QAP_T4036
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4016 import QAP_T4016
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4015 import QAP_T4015
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4014 import QAP_T4014
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4013 import QAP_T4013
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4012 import QAP_T4012
from test_cases.web_admin.web_admin_test_cases.others.QAP_T4011 import QAP_T4011
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer

from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.others.QAP_T3405 import QAP_T3405


class RunOthers:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Others", root_report_id)
        self.web_driver_container = None

    def execute(self):

        try:
            configuration = ComponentConfiguration("WA_Others")  # look at xml (component name="web_admin_general")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_T4039(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4038(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4037(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4036(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4016(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4015(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4014(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4013(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4012(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T4011(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                    environment=configuration.environment).run()
            QAP_T3973(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3972(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3970(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3966(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3889(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3888(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3834(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3833(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3824(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3678(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3677(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3573(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3545(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3476(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_T3405(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Others ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
            print("--RunOthers finished--")
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
