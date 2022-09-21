import time
import traceback

from datetime import timedelta
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3334 import QAP_T3334
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3354 import QAP_T3354
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3355 import QAP_T3355
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3524 import QAP_T3524
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3575 import QAP_T3575
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3710 import QAP_T3710
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3795 import QAP_T3795
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3822 import QAP_T3822
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3823 import QAP_T3823
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3842 import QAP_T3842
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3852 import QAP_T3852
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3858 import QAP_T3858
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3859 import QAP_T3859
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3860 import QAP_T3860
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3880 import QAP_T3880
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3890 import QAP_T3890
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3893 import QAP_T3893
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3896 import QAP_T3896
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3897 import QAP_T3897
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3906 import QAP_T3906
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3922 import QAP_T3922
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3926 import QAP_T3926
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3928 import QAP_T3928
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3931 import QAP_T3931
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3935 import QAP_T3935
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3951 import QAP_T3951
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3957 import QAP_T3957
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3960 import QAP_T3960
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3961 import QAP_T3961
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3962 import QAP_T3962
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3963 import QAP_T3963
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3964 import QAP_T3964
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3965 import QAP_T3965
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3967 import QAP_T3967
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3968 import QAP_T3968
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3969 import QAP_T3969
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3984 import QAP_T3984
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3986 import QAP_T3986
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3987 import QAP_T3987
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3988 import QAP_T3988
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3989 import QAP_T3989
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3990 import QAP_T3990
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T3991 import QAP_T3991
from test_cases.web_admin.web_admin_test_cases.market_making.QAP_T7868 import QAP_T7868


class RunMarketMaking:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WA_Market_Making", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_Market_Making")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[0].web_browser,
                configuration.environment.get_list_web_admin_environment()[0].site_url)
            start_time = time.monotonic()
            QAP_T3334(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3354(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3355(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3524(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3575(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3710(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3795(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3822(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3823(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3842(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3852(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3858(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3859(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3860(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3880(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3890(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3893(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3896(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3897(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3906(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3922(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3926(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3928(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3931(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3935(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3951(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3957(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3960(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3961(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3962(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3963(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3964(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3965(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3967(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3968(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3969(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3984(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3986(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3987(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3988(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3989(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3990(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3991(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T7868(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run FXMM ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
