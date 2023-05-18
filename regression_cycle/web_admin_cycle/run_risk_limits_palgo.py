import time
import traceback

from datetime import timedelta
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca

from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3143 import QAP_T3143
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3204 import QAP_T3204
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3205 import QAP_T3205
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3218 import QAP_T3218
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3230 import QAP_T3230
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3264 import QAP_T3264
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3272 import QAP_T3272
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3273 import QAP_T3273
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3294 import QAP_T3294
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3322 import QAP_T3322
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3335 import QAP_T3335
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3336 import QAP_T3336
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3337 import QAP_T3337
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3339 import QAP_T3339
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3359 import QAP_T3359
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3360 import QAP_T3360
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3414 import QAP_T3414
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3461 import QAP_T3461
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3462 import QAP_T3462
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3591 import QAP_T3591
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3592 import QAP_T3592
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3594 import QAP_T3594
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3664 import QAP_T3664
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3665 import QAP_T3665
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3674 import QAP_T3674
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3675 import QAP_T3675
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3676 import QAP_T3676
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3691 import QAP_T3691
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3729 import QAP_T3729
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3768 import QAP_T3768
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T3917 import QAP_T3917
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T4019 import QAP_T4019
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T4020 import QAP_T4020
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T7931 import QAP_T7931
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T7933 import QAP_T7933
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T7934 import QAP_T7934
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T9298 import QAP_T9298
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T9330 import QAP_T9330
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T10574 import QAP_T10574
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T10583 import QAP_T10583
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T10584 import QAP_T10584
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T10586 import QAP_T10586
from test_cases.web_admin.web_admin_test_cases.risk_limits.QAP_T10814 import QAP_T10814


class RunRiskLimits:
    def __init__(self, root_report_id, mode, version):
        if mode == 'Regression':
            self.second_lvl_id = bca.create_event(f"WA_RiskLimits" if version is None else f"WA_RiskLimits | {version}", root_report_id)
        else:
            self.second_lvl_id = bca.create_event(f"WA_RiskLimits (verification)" if version is None else f"WA_RiskLimits (verification) | {version}", root_report_id)

        self.web_driver_container = None

    def execute(self):
        try:
            configuration = ComponentConfiguration("WA_PALGO")  # look at xml (component name="web_admin_general")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_admin_environment()[1].web_browser,
                configuration.environment.get_list_web_admin_environment()[1].site_url)
            start_time = time.monotonic()
            # QAP_T3143(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T3204(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3205(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # QAP_T3218(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3230(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3264(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3272(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3273(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3294(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3322(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T3335(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # QAP_T3336(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3337(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3339(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T3359(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3360(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # QAP_T3414(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T3461(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # QAP_T3462(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3591(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3592(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3594(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3664(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T3665(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            # QAP_T3674(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3675(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3676(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3691(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3729(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3768(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T3917(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T4019(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T4020(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T7931(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T7933(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T7934(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T9298(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            # QAP_T9330(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #           environment=configuration.environment).run()
            QAP_T10574(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            # QAP_T10583(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #            environment=configuration.environment).run()
            QAP_T10584(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10586(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()
            QAP_T10814(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                       environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run Risk Limits ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
