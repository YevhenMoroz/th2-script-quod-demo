import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.portfolio.QAP_T7793 import QAP_T7793
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.configurations.component_configuration import ComponentConfiguration


class Mobile_Portfolio:
    def __init__(self, driver: AppiumDriver, parent_id, version=None):
        self.folder_name = 'FEMobile'
        self.report_id = bca.create_event("Mobile_Portfolio", parent_id)
        self.appium_driver = driver

    def execute(self):
        try:
            configuration = ComponentConfiguration("Mobile_Portfolio")
            QAP_T7793(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
