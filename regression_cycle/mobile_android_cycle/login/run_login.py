import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.loginlogout.QAP_T3432 import QAP_T3432
from test_cases.mobile_android.pages.loginlogout.QAP_T3374 import QAP_T3374
from test_cases.mobile_android.pages.loginlogout.QAP_T3373 import QAP_T3373
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.configurations.component_configuration import ComponentConfiguration


class RunLogin:
    def __init__(self, driver: AppiumDriver, root_report_id):
        self.folder_name = 'FEMobile'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.appium_driver = driver

    def execute(self):
        try:
            configuration = ComponentConfiguration("Mobile_LoginLogout")
            # QAP_T3467(self.appium_driver, self.second_lvl_id).run()
            # QAP_T3432(self.appium_driver, self.second_lvl_id).run()
            # QAP_T3375(self.appium_driver, self.second_lvl_id).run()
            QAP_T3374(self.appium_driver, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            # QAP_T3373(self.appium_driver, self.second_lvl_id).run()
            # QAP_T3372(self.appium_driver, self.second_lvl_id).run()
            # QAP_T3371(self.appium_driver, self.second_lvl_id).run()
            # QAP_T3370(self.appium_driver, self.second_lvl_id).run()
            # QAP_T3369(self.appium_driver, self.second_lvl_id).run()
        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
