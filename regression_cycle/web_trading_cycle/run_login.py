import time
import traceback
from datetime import timedelta

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca
from test_cases.web_trading.test_cases.pages.main_page.menu.QAP_6286 import QAP_6286
from test_cases.web_trading.test_cases.pages.main_page.menu.QAP_6287 import QAP_6287


class RunLogin:
    def __init__(self, web_driver_container: WebDriverContainer, root_report_id):
        self.folder_name = 'WebTrading'
        self.first_lvl_id = bca.create_event(self.__class__.__name__, root_report_id)
        self.second_lvl_id = bca.create_event(self.folder_name, self.first_lvl_id)
        self.web_driver_container = web_driver_container

    def execute(self):
        try:
            start_time = time.monotonic()

            # QAP_6296(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6436(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6568(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6634(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6635(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6637(self.web_driver_container, self.second_lvl_id).run()
            # QAP_6639(self.web_driver_container, self.second_lvl_id).run()
            QAP_6286(self.web_driver_container, self.second_lvl_id).run()
            QAP_6287(self.web_driver_container, self.second_lvl_id).run()


            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
