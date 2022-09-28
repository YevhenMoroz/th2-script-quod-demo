import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.loginlogout.QAP_T3375 import QAP_T3375
from test_cases.mobile_android.pages.market.QAP_T3368 import QAP_T3368
from test_cases.mobile_android.pages.market.QAP_T3381 import QAP_T3381
from test_cases.mobile_android.pages.market.QAP_T3382 import QAP_T3382
from test_cases.mobile_android.pages.market.QAP_T3383 import QAP_T3383
from test_cases.mobile_android.pages.market.QAP_T3384 import QAP_T3384
from test_cases.mobile_android.pages.market.QAP_T3385 import QAP_T3385
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.configurations.component_configuration import ComponentConfiguration


class Mobile_Market:
    def __init__(self, driver: AppiumDriver, parent_id, version=None):
        self.folder_name = 'FEMobile'
        self.report_id = bca.create_event("Mobile_Market", parent_id)
        self.appium_driver = driver

    def execute(self):
        try:
            configuration = ComponentConfiguration("Mobile_Market")
            QAP_T3368(self.appium_driver, self.report_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3381(self.appium_driver, self.report_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3382(self.appium_driver, self.report_id, data_set=configuration.data_set,
                  environment=configuration.environment).run()
            QAP_T3383(self.appium_driver, self.report_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3384(self.appium_driver, self.report_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
            QAP_T3385(self.appium_driver, self.report_id, data_set=configuration.data_set,
                      environment=configuration.environment).run()
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
