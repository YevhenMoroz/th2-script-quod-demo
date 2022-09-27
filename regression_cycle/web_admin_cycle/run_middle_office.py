import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3114 import QAP_T3114
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3124 import QAP_T3124
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3242 import QAP_T3242
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3243 import QAP_T3243
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3290 import QAP_T3290
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3390 import QAP_T3390
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3408 import QAP_T3408
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3446 import QAP_T3446
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3448 import QAP_T3448
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3586 import QAP_T3586
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3587 import QAP_T3587
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3628 import QAP_T3628
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3686 import QAP_T3686
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3794 import QAP_T3794
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3814 import QAP_T3814
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3815 import QAP_T3815
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3816 import QAP_T3816
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3825 import QAP_T3825
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3826 import QAP_T3826
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3827 import QAP_T3827
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3828 import QAP_T3828
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3829 import QAP_T3829
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3837 import QAP_T3837
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3839 import QAP_T3839
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3840 import QAP_T3840
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3841 import QAP_T3841
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3843 import QAP_T3843
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3845 import QAP_T3845
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3847 import QAP_T3847
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3856 import QAP_T3856
from test_cases.web_admin.web_admin_test_cases.middle_office.QAP_T3905 import QAP_T3905


class RunMiddleOffice:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Middle_Office", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Middle_Office")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_T3114(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3124(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3242(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3243(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3290(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3390(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3408(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3446(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3448(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3586(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3587(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3628(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3686(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3794(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3814(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3815(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3816(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3825(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3826(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3827(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3828(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3829(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3837(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3839(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3840(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3841(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3843(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3845(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3847(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3856(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3905(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Middle Office ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
