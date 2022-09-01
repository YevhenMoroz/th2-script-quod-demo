import time
import traceback
from datetime import timedelta


from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca



class RunOther:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WebTrading_Other", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            start_time = time.monotonic()
            configuration = ComponentConfiguration("WebTrading_Other")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_trading_environment()[0].web_browser,
                configuration.environment.get_list_web_trading_environment()[0].site_url)

            end_time = time.monotonic()
            print("Run Other ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
