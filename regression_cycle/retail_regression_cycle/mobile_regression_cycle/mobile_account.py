import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.account.QAP_T3276 import QAP_T3276
from test_cases.mobile_android.pages.account.QAP_T3362 import QAP_T3362
from test_cases.mobile_android.pages.account.QAP_T3425 import QAP_T3425
from test_cases.mobile_android.pages.account.QAP_T3456 import QAP_T3456
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.configurations.component_configuration import ComponentConfiguration


class Mobile_Account:
    def __init__(self, driver: AppiumDriver, parent_id, version=None):
        self.folder_name = 'FEMobile'
        self.report_id = bca.create_event("Mobile_Account", parent_id)
        self.appium_driver = driver

    def execute(self):
        try:
            configuration = ComponentConfiguration("Mobile_Account")
            QAP_T3276(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()
            QAP_T3362(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()
            QAP_T3425(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()
            QAP_T3456(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
