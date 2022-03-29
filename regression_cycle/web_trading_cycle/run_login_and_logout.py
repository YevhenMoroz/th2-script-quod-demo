import time
import traceback
from datetime import timedelta

from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_6296 import QAP_6296
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_6634 import QAP_6634
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_6635 import QAP_6635
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_6637 import QAP_6637
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_6639 import QAP_6639
from test_cases.web_trading.test_cases.pages.main_page.user_profile.QAP_6286 import QAP_6286
from test_cases.web_trading.test_cases.pages.main_page.user_profile.QAP_6287 import QAP_6287
from test_cases.web_trading.test_cases.pages.main_page.workspace.order_ticket_and_book.QAP_6568 import QAP_6568
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca



class RunLoginAndLogout:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WebTradingLoginAndLogout", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            start_time = time.monotonic()
            configuration = ComponentConfiguration("WebTradingLoginAndLogout")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_trading_environment()[0].web_browser,
                configuration.environment.get_list_web_trading_environment()[0].site_url)

            QAP_6296(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            # QAP_6436(self.web_driver_container, self.second_lvl_id).run()
            QAP_6568(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6634(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6635(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6637(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6639(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6286(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            QAP_6287(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()

            end_time = time.monotonic()
            print("Run General ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
