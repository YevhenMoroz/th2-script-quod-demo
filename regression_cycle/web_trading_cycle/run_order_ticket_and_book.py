import time
import traceback
from datetime import timedelta

from test_cases.web_trading.test_cases.pages.main_page.workspace.order_ticket_and_book.QAP_T3427 import QAP_T3427
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from custom import basic_custom_actions as bca



class RunOrderTicketAndBook:
    def __init__(self, root_report_id):
        self.second_lvl_id = bca.create_event("WebTrading_OrderTicket_And_Book", root_report_id)
        self.web_driver_container = None

    def execute(self):
        try:
            start_time = time.monotonic()
            configuration = ComponentConfiguration("WebTrading_OrderTicket_And_Book")
            self.web_driver_container = WebDriverContainer(
                configuration.environment.get_list_web_trading_environment()[0].web_browser,
                configuration.environment.get_list_web_trading_environment()[0].site_url)
            QAP_T3427(self.web_driver_container, self.second_lvl_id, data_set=configuration.data_set,
                     environment=configuration.environment).run()
            end_time = time.monotonic()
            print("Run Order Ticket And Book ~execution time~ = " + str(timedelta(seconds=end_time - start_time)))

        except Exception:
            print(traceback.format_exc() + " Execute ERROR !->  " + self.__class__.__name__)
