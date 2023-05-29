import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_test_cases.general.QAP_T3253 import QAP_T3253
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3254 import QAP_T3254
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3255 import QAP_T3255
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3351 import QAP_T3351
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3507 import QAP_T3507
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3517 import QAP_T3517
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3539 import QAP_T3539
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3566 import QAP_T3566
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3681 import QAP_T3681
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3797 import QAP_T3797
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3855 import QAP_T3855
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3881 import QAP_T3881
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3894 import QAP_T3894
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3895 import QAP_T3895
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3898 import QAP_T3898
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3899 import QAP_T3899
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3904 import QAP_T3904
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3907 import QAP_T3907
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3908 import QAP_T3908
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3910 import QAP_T3910
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3918 import QAP_T3918
from test_cases.web_admin.web_admin_test_cases.general.QAP_T3921 import QAP_T3921
from test_cases.web_admin.web_admin_test_cases.general.QAP_T4017 import QAP_T4017
from test_cases.web_admin.web_admin_test_cases.general.QAP_T4018 import QAP_T4018
from test_cases.web_admin.web_admin_test_cases.general.QAP_T7866 import QAP_T7866
from test_cases.web_admin.web_admin_test_cases.general.QAP_T8840 import QAP_T8840
from test_cases.web_admin.web_admin_test_cases.general.QAP_T8935 import QAP_T8935
from test_cases.web_admin.web_admin_test_cases.general.QAP_T9446 import QAP_T9446
from test_cases.web_admin.web_admin_test_cases.general.QAP_T10424 import QAP_T10424
from test_cases.web_admin.web_admin_test_cases.general.QAP_T10643 import QAP_T10643


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

            QAP_T3253(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3254(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3255(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3351(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3507(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3517(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3539(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3566(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3681(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3797(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3855(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3881(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3894(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3895(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3898(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3899(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3904(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3907(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3908(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3910(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3918(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3921(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4017(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4018(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7866(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            #Waiting resolving PEQ-11597
            # QAP_T8840(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T8935(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T9446(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T10424(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10643(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
