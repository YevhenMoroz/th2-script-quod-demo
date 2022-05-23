import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.login.QAP_6491 import QAP_6491
from test_cases.mobile_android.pages.login.QAP_6877 import QAP_6877
from test_cases.mobile_android.pages.login.QAP_6878 import QAP_6878
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class RunLogin:
    def __init__(self, driver: AppiumDriver, root_report_id):
        self.folder_name = 'FEMobile'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.appium_driver = driver

    def execute(self):
        try:
            # QAP_6348(self.appium_driver, self.second_lvl_id).run()
            # QAP_6491(self.appium_driver, self.second_lvl_id).run()
            # QAP_6876(self.appium_driver, self.second_lvl_id).run()
            QAP_6877(self.appium_driver, self.second_lvl_id).run()
            # QAP_6878(self.appium_driver, self.second_lvl_id).run()
            # QAP_6879(self.appium_driver, self.second_lvl_id).run()
            # QAP_6880(self.appium_driver, self.second_lvl_id).run()
            # QAP_6881(self.appium_driver, self.second_lvl_id).run()
            # QAP_6882(self.appium_driver, self.second_lvl_id).run()
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
