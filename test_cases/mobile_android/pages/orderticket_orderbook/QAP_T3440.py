from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage
from test_framework.mobile_android_core.pages.market.market_page import MarketPage

from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage
from test_framework.mobile_android_core.pages.order_ticket.order_ticket_constants import OrderTicketConstants
from test_framework.mobile_android_core.pages.order_ticket.order_ticket_page import OrderTicketPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T3440(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.instrument_1 = self.data_set.get_instrument("instrument_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        market_page = MarketPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)
        order_ticket_page = OrderTicketPage(self.appium_driver)
        login_page.login_to_mobile_trading(self.login, self.password)
        self.verify("Precondition - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion
        # region - test details

        # Step 1
        main_page.click_on_portfolio()
        main_page.click_on_create_new_order()
        self.verify("Step 1 - OrderTicket is opened gtom Portfolio", None, main_page.wait_element_presence(OrderTicketConstants.ORDER_TICKET_TITLE))
        # endregion

        # Step 2
        order_ticket_page.click_back_button()
        main_page.click_on_market()
        main_page.click_on_create_new_order()
        self.verify("Step 2 - OrderTicket is opened from Market", None,
                    main_page.wait_element_presence(OrderTicketConstants.ORDER_TICKET_TITLE))
        # endregion

        # Step 3
        order_ticket_page.click_back_button()
        main_page.click_on_orders()
        main_page.click_on_create_new_order()
        self.verify("Step 3 - OrderTicket is opened from Orders", None,
                    main_page.wait_element_presence(OrderTicketConstants.ORDER_TICKET_TITLE))
        # endregion

        # Step 4
        order_ticket_page.click_back_button()
        main_page.click_on_news()
        main_page.click_on_create_new_order()
        self.verify("Step 4 - OrderTicket is opened from News", None,
                    main_page.wait_element_presence(OrderTicketConstants.ORDER_TICKET_TITLE))
        # endregion