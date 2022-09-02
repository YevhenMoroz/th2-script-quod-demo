import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.loginlogout.QAP_T3375 import QAP_T3375
from test_cases.mobile_android.pages.market.QAP_T3382 import QAP_T3382
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.configurations.component_configuration import ComponentConfiguration


class Mobile_Market:
    def __init__(self, driver: AppiumDriver, parent_id, version=None):
        self.folder_name = 'FEMobile'
        self.cycle_name = 'V172_Mobile'
        self.report_id = bca.create_event("Mobile_LoginLogout", parent_id)
        self.appium_driver = driver

    def execute(self):
        try:
            configuration = ComponentConfiguration("Mobile_Market")
            # QAP_T3375(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()
            QAP_T3382(self.appium_driver, self.report_id, data_set=configuration.data_set,
                  environment=configuration.environment).run()
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
