import time
import traceback
from datetime import timedelta

from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3487 import QAP_T3487
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3426 import QAP_T3426
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3419 import QAP_T3419
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3418 import QAP_T3418
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3417 import QAP_T3417
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3416 import QAP_T3416
from test_cases.web_trading.test_cases.pages.login_and_logout.QAP_T3415 import QAP_T3415
from test_cases.web_trading.test_cases.pages.main_page.user_profile.QAP_T3491 import QAP_T3491
from test_cases.web_trading.test_cases.pages.main_page.workspace.order_ticket_and_book.QAP_T3421 import QAP_T3421
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca



class RunLoginAndLogout:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WebTrading_Login_And_Logout", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            start_time = time.monotonic()
            configuration = ComponentConfiguration("WebTrading_Login_And_Logout")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_trading_environment()[0].web_browser,
                configuration.environment.get_list_web_trading_environment()[0].site_url)

            # QAP_T3487(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_6436(self.web_driver_container, self.second_lvl_id).run()
            # QAP_T3421(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            QAP_T3426(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            # QAP_T3419(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_T3418(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_T3417(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_T3416(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_T3492(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_T3491(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            # QAP_T3415(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
            #          environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Login And Logout ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
