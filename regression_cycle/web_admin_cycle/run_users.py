import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import WebAdminComponentConfiguration
from test_framework.db_wrapper.db_manager import DBManager
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
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3654 import QAP_T3654
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3655 import QAP_T3655
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3656 import QAP_T3656
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3657 import QAP_T3657
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3658 import QAP_T3658
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3659 import QAP_T3659
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3679 import QAP_T3679
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3688 import QAP_T3688
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3690 import QAP_T3690
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3693 import QAP_T3693
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3718 import QAP_T3718
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3720 import QAP_T3720
from test_cases.web_admin.web_admin_test_cases.users.QAP_T3763 import QAP_T3763
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
from test_cases.web_admin.web_admin_test_cases.users.QAP_T9421 import QAP_T9421
from test_cases.web_admin.web_admin_test_cases.users.QAP_T9443 import QAP_T9443
from test_cases.web_admin.web_admin_test_cases.users.QAP_T8890 import QAP_T8890
from test_cases.web_admin.web_admin_test_cases.users.QAP_T8891 import QAP_T8891
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10304 import QAP_T10304
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10305 import QAP_T10305
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10309 import QAP_T10309
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10310 import QAP_T10310
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10311 import QAP_T10311
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10312 import QAP_T10312
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10316 import QAP_T10316
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10317 import QAP_T10317
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10318 import QAP_T10318
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10320 import QAP_T10320
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10321 import QAP_T10321
#from test_cases.web_admin.web_admin_test_cases.users.QAP_T10306 import QAP_T10306
from test_cases.web_admin.web_admin_test_cases.users.QAP_T10834 import QAP_T10834
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11142 import QAP_T11142
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11206 import QAP_T11206
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11215 import QAP_T11215
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11232 import QAP_T11232
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11252 import QAP_T11252
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11287 import QAP_T11287
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11288 import QAP_T11288
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11289 import QAP_T11289
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11585 import QAP_T11585
from test_cases.web_admin.web_admin_test_cases.users.QAP_T11694 import QAP_T11694


class RunUsers:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Users", root_report_id)
        self.web_driver_container = None
        self.db_manager = None

    def execute(self):
        try:
            configuration = WebAdminComponentConfiguration("WA_Users")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            self.db_manager = DBManager(configuration.environment.get_list_data_base_environment()[0])

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
            QAP_T3654(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment, db_manager=self.db_manager).run()
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
            QAP_T3690(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment, db_manager=self.db_manager).run()
            QAP_T3693(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3718(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3720(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3763(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
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
            QAP_T3903(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # QAP_T3920(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
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
            QAP_T8890(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8891(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T9421(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment, db_manager=self.db_manager).run()
            QAP_T9443(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T10304(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10305(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10309(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10310(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10311(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10312(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10316(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10317(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10318(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10320(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10321(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            # QAP_T10306(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #            environment=configuration.environment).run()
            QAP_T10834(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T11142(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T11252(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T11206(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment, db_manager=self.db_manager).run()
            QAP_T11215(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T11232(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment, db_manager=self.db_manager).run()
            QAP_T11287(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment, db_manager=self.db_manager).run()
            QAP_T11288(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T11289(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment, db_manager=self.db_manager).run()
            QAP_T11585(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T11694(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Users ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
