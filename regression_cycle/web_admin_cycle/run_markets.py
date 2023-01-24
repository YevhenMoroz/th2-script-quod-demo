import time
import traceback
from datetime import timedelta

from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3115 import QAP_T3115
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3118 import QAP_T3118
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3237 import QAP_T3237
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3247 import QAP_T3247
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3240 import QAP_T3240
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3248 import QAP_T3248
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3249 import QAP_T3249
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3250 import QAP_T3250
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3289 import QAP_T3289
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3293 import QAP_T3293
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3295 import QAP_T3295
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3297 import QAP_T3297
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3358 import QAP_T3358
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3403 import QAP_T3403
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3449 import QAP_T3449
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3450 import QAP_T3450
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3451 import QAP_T3451
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3465 import QAP_T3465
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3484 import QAP_T3484
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3485 import QAP_T3485
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3545 import QAP_T3545
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3550 import QAP_T3550
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3573 import QAP_T3573
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3574 import QAP_T3574
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3677 import QAP_T3677
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3678 import QAP_T3678
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3683 import QAP_T3683
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3684 import QAP_T3684
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3698 import QAP_T3698
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3719 import QAP_T3719
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3772 import QAP_T3772
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3784 import QAP_T3784
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3785 import QAP_T3785
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3793 import QAP_T3793
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3799 import QAP_T3799
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3801 import QAP_T3801
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3817 import QAP_T3817
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3836 import QAP_T3836
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3838 import QAP_T3838
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3848 import QAP_T3848
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3862 import QAP_T3862
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3873 import QAP_T3873
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3874 import QAP_T3874
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3875 import QAP_T3875
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3911 import QAP_T3911
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3930 import QAP_T3930
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3952 import QAP_T3952
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3966 import QAP_T3966
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3970 import QAP_T3970
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3972 import QAP_T3972
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3973 import QAP_T3973
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3974 import QAP_T3974
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3975 import QAP_T3975
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3976 import QAP_T3976
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3977 import QAP_T3977
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3978 import QAP_T3978
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3980 import QAP_T3980
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T3981 import QAP_T3981
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4011 import QAP_T4011
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4012 import QAP_T4012
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4013 import QAP_T4013
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4028 import QAP_T4028
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4029 import QAP_T4029
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4030 import QAP_T4030
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4031 import QAP_T4031
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4032 import QAP_T4032
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4033 import QAP_T4033
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4034 import QAP_T4034
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4035 import QAP_T4035
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T4036 import QAP_T4036
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T7872 import QAP_T7872
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T7932 import QAP_T7932
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T8293 import QAP_T8293
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T8808 import QAP_T8808
from test_cases.web_admin.web_admin_test_cases.markets.QAP_T8895 import QAP_T8895


class RunMarkets:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Markets", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Markets")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()

            QAP_T3115(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3118(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3237(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3247(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3240(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3248(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3249(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3250(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3289(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3293(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3295(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3297(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3358(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3403(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3449(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3450(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3451(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3465(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3484(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3485(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3545(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3550(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3573(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3574(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3677(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3678(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3683(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3684(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3698(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3719(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3772(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3784(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3785(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3793(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3799(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3801(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3817(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3836(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3838(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3848(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3862(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # Need refactoring
            QAP_T3873(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # Need refactoring
            QAP_T3874(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3875(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3911(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3930(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3952(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3966(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3970(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3972(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3973(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3974(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3975(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3976(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3977(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3978(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3980(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3981(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4011(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4012(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4013(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4028(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4029(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4030(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4031(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4032(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4033(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4034(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4035(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T4036(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7932(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7872(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8293(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8808(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T8895(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Markets ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
