import traceback
from custom import basic_custom_actions as bca
from test_cases.mobile_android.pages.loginlogout.QAP_T3375 import QAP_T3375
from test_cases.mobile_android.pages.orderticket_orderbook.QAP_T3440 import QAP_T3440
from test_framework.mobile_android_core.utils.driver import AppiumDriver
from test_framework.configurations.component_configuration import ComponentConfiguration


class Mobile_OrderTicket_OrderBook:
    def __init__(self, driver: AppiumDriver, parent_id, version=None):
        self.folder_name = 'FEMobile'
        self.report_id = bca.create_event("Mobile_OrderTicket_OrderBook", parent_id)
        self.appium_driver = driver

    def execute(self):
        try:
            configuration = ComponentConfiguration("Mobile_OrderTicket_OrderBook")
            QAP_T3440(self.appium_driver, self.report_id, data_set=configuration.data_set, environment=configuration.environment).run()

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
