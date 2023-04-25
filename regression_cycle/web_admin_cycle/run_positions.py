import time
import traceback

from datetime import timedelta
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3340 import QAP_T3340
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3342 import QAP_T3342
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3352 import QAP_T3352
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3389 import QAP_T3389
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3393 import QAP_T3393
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3394 import QAP_T3394
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3395 import QAP_T3395
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3396 import QAP_T3396
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3397 import QAP_T3397
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3404 import QAP_T3404
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3406 import QAP_T3406
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3412 import QAP_T3412
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3430 import QAP_T3430
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3470 import QAP_T3470
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3486 import QAP_T3486
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3496 import QAP_T3496
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3497 import QAP_T3497
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3498 import QAP_T3498
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3632 import QAP_T3632
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3634 import QAP_T3634
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3809 import QAP_T3809
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3946 import QAP_T3946
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3947 import QAP_T3947
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3948 import QAP_T3948
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T3949 import QAP_T3949
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T7795 import QAP_T7795
from test_cases.web_admin.web_admin_test_cases.positions.QAP_T7796 import QAP_T7796


class RunPositions:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Positions", root_report_id)
        self.web_driver_container = None
        self.db_manager = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Positions")  # look at xml (component name="web_admin_general")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[1].site_url)
            self.db_manager = DBManager(configuration.environment.get_list_data_base_environment()[1])

            start_time = time.monotonic()

            QAP_T3352(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3393(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3394(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3395(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3396(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3397(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment, db_manager=self.db_manager).run()
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
            QAP_T7796(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            # ATs that do not work on the quod306 site must be run on a site with a running RDS component
            # QAP_T3340(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3342(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3470(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment, db_manager=self.db_manager).run()
            # QAP_T3389(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3496(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3497(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3498(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment, db_manager=self.db_manager).run()


            end_time = time.monotonic()
            print("Run Positions ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
