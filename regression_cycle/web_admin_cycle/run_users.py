import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.users.QAP_T3292 import QAP_T3292
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3531 import QAP_T3531
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3565 import QAP_T3565
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3602 import QAP_T3602
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3621 import QAP_T3621
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3623 import QAP_T3623
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3625 import QAP_T3625
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3627 import QAP_T3627
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3651 import QAP_T3651
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3655 import QAP_T3655
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3656 import QAP_T3656
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3657 import QAP_T3657
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3658 import QAP_T3658
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3659 import QAP_T3659
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3679 import QAP_T3679
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3688 import QAP_T3688
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3693 import QAP_T3693
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3718 import QAP_T3718
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3720 import QAP_T3720
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3777 import QAP_T3777
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3782 import QAP_T3782
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3803 import QAP_T3803
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3808 import QAP_T3808
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3846 import QAP_T3846
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3851 import QAP_T3851
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3876 import QAP_T3876
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3903 import QAP_T3903
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3920 import QAP_T3920
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3925 import QAP_T3925
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3932 import QAP_T3932
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3933 import QAP_T3933
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3934 import QAP_T3934
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3993 import QAP_T3993
from test_cases.web_admin.web_admin_test_cases.users.QAP_T4009 import QAP_T4009
from test_cases.web_admin.web_admin_test_cases.users.QAP_T4010 import QAP_T4010
from test_cases.web_admin.web_admin_test_cases.users.QAP_T7871 import QAP_T7871
from test_cases.web_admin.web_admin_test_cases.users.QAP_T7874 import QAP_T7874


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
            QAP_T3292(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3531(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3565(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3602(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3621(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3623(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3625(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3627(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3651(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3655(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3656(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3657(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3658(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3659(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3679(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3688(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3693(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3718(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3720(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3777(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3782(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3803(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3808(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3846(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3851(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3876(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3903(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3920(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3925(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3932(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3933(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3934(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3993(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4009(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4010(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7871(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7874(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Users ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
