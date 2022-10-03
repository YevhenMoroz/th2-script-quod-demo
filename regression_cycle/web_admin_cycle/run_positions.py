import time
import traceback

from datetime import timedelta
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3404 import QAP_T3404
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3406 import QAP_T3406
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3412 import QAP_T3412
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3430 import QAP_T3430
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3486 import QAP_T3486
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3632 import QAP_T3632
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3634 import QAP_T3634
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3809 import QAP_T3809
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3946 import QAP_T3946
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3947 import QAP_T3947
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3948 import QAP_T3948
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3949 import QAP_T3949
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T7795 import QAP_T7795


class RunPositions:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Positions", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Positions")  # look at xml (component name="web_admin_general")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()

            QAP_T3404(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3406(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3412(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3430(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3486(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3632(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3634(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3809(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3946(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3947(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3948(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3949(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7795(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Positions ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
