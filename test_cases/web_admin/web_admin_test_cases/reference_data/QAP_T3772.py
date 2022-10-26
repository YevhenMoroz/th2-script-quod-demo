import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard \
    import VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_wizard import VenuesWizard
from test_framework.web_admin_core.pages.markets.venues.venues_support_feed_types_sub_wizard \
    import VenuesSupportFeedTypesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3772(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.test_venue = ''
        self.support_feed_types = {"Status": '', "Quote": '', "Quote Book": '', "Tickers": '', "Market Time": '',
                                   "Discretion Inst": '', "Broker Queue": '', "Market Depth": '', "Movers": '',
                                   "News": '', "Term Quote Request": '', "Quote Cancel": '', "Intraday": '',
                                   "Order Book": '', "Times And Sales": '', "Trade": '', "Sized MD Request": ''}

        self.actual_result = dict()

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_venues_page()

    def test_context(self):
        try:
            self.precondition()

            page = VenuesPage(self.web_driver_container)
            page.click_on_more_actions()
            page.click_on_edit()
            values_tab = VenuesValuesSubWizard(self.web_driver_container)
            self.test_venue = values_tab.get_name()

            support_feed_tab = VenuesSupportFeedTypesSubWizard(self.web_driver_container)
            support_feed_tab.click_on_status()
            support_feed_tab.click_on_quote()
            support_feed_tab.click_on_quote_book()
            support_feed_tab.click_on_tickers()
            support_feed_tab.click_on_market_time()
            support_feed_tab.click_on_discretion_inst()
            support_feed_tab.click_on_broker_queue()
            support_feed_tab.click_on_market_depth()
            support_feed_tab.click_on_movers()
            support_feed_tab.click_on_news()
            support_feed_tab.click_on_term_quote_request()
            support_feed_tab.click_on_quote_cancel()
            support_feed_tab.click_on_intraday()
            support_feed_tab.click_on_order_book()
            support_feed_tab.click_on_times_and_sales()
            support_feed_tab.click_on_trade()
            support_feed_tab.click_on_sized_md_request()

            self.support_feed_types["Status"] = support_feed_tab.is_status_selected()
            self.support_feed_types["Quote"] = support_feed_tab.is_quote_selected()
            self.support_feed_types["Quote Book"] = support_feed_tab.is_quote_book_selected()
            self.support_feed_types["Tickers"] = support_feed_tab.is_tickers_selected()
            self.support_feed_types["Market Time"] = support_feed_tab.is_market_time_selected()
            self.support_feed_types["Discretion Inst"] = support_feed_tab.is_discretion_inst_selected()
            time.sleep(2)
            self.support_feed_types["Broker Queue"] = support_feed_tab.is_broker_queue()
            self.support_feed_types["Market Depth"] = support_feed_tab.is_market_depth_selected()
            self.support_feed_types["Movers"] = support_feed_tab.is_movers_selected()
            self.support_feed_types["News"] = support_feed_tab.is_news_selected()
            self.support_feed_types["Term Quote Request"] = support_feed_tab.is_term_quote_request_selected()
            self.support_feed_types["Quote Cancel"] = support_feed_tab.is_quote_cancel_selected()
            self.support_feed_types["Intraday"] = support_feed_tab.is_intraday_selected()
            self.support_feed_types["Order Book"] = support_feed_tab.is_order_book_selected()
            self.support_feed_types["Times And Sales"] = support_feed_tab.is_times_and_sales_selected()
            self.support_feed_types["Trade"] = support_feed_tab.is_trade_selected()
            self.support_feed_types["Sized MD Request"] = support_feed_tab.is_sized_md_request_selected()

            wizard = VenuesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            page.set_name_filter(self.test_venue)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            self.actual_result["Status"] = support_feed_tab.is_status_selected()
            self.actual_result["Quote"] = support_feed_tab.is_quote_selected()
            self.actual_result["Quote Book"] = support_feed_tab.is_quote_book_selected()
            self.actual_result["Tickers"] = support_feed_tab.is_tickers_selected()
            self.actual_result["Market Time"] = support_feed_tab.is_market_time_selected()
            self.actual_result["Discretion Inst"] = support_feed_tab.is_discretion_inst_selected()
            self.actual_result["Broker Queue"] = support_feed_tab.is_broker_queue()
            self.actual_result["Market Depth"] = support_feed_tab.is_market_depth_selected()
            self.actual_result["Movers"] = support_feed_tab.is_movers_selected()
            self.actual_result["News"] = support_feed_tab.is_news_selected()
            self.actual_result["Term Quote Request"] = support_feed_tab.is_term_quote_request_selected()
            self.actual_result["Quote Cancel"] = support_feed_tab.is_quote_cancel_selected()
            self.actual_result["Intraday"] = support_feed_tab.is_intraday_selected()
            self.actual_result["Order Book"] = support_feed_tab.is_order_book_selected()
            self.actual_result["Times And Sales"] = support_feed_tab.is_times_and_sales_selected()
            self.actual_result["Trade"] = support_feed_tab.is_trade_selected()
            self.actual_result["Sized MD Request"] = support_feed_tab.is_sized_md_request_selected()
            time.sleep(1)

            self.verify("All changes for checkboxes saved correct", self.support_feed_types, self.actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
