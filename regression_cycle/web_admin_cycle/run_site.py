import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3127 import QAP_T3127
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3468 import QAP_T3468
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3576 import QAP_T3576
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3577 import QAP_T3577
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3578 import QAP_T3578
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3579 import QAP_T3579
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3582 import QAP_T3582
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3584 import QAP_T3584
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3585 import QAP_T3585
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3590 import QAP_T3590
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3595 import QAP_T3595
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3596 import QAP_T3596
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3597 import QAP_T3597
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3598 import QAP_T3598
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3599 import QAP_T3599
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3645 import QAP_T3645
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3650 import QAP_T3650
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3652 import QAP_T3652
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3692 import QAP_T3692
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3694 import QAP_T3694
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3695 import QAP_T3695
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3696 import QAP_T3696
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3697 import QAP_T3697
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3699 import QAP_T3699
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3700 import QAP_T3700
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3701 import QAP_T3701
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3702 import QAP_T3702
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3703 import QAP_T3703
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3704 import QAP_T3704
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3786 import QAP_T3786
from test_cases.web_admin.web_admin_test_cases.site.QAP_T3787 import QAP_T3787


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

            QAP_T3127(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3468(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3650(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3576(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3577(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3578(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3579(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3582(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3584(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3585(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3590(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3595(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3596(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3597(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3598(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3599(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3645(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3652(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3692(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3694(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3695(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3696(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3697(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3699(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3700(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3701(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3702(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3703(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3704(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3786(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3787(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Site ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
