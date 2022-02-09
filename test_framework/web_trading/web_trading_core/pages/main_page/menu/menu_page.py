from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_constants import MenuConstants


class MenuPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_profile_button(self):
        self.find_by_xpath(MenuConstants.PROFILE_BUTTON_XPATH).click()

    def click_on_hide_header_button(self):
        self.find_by_xpath(MenuConstants.HIDE_HEADER_BUTTON_XPATH).click()

    def click_on_dark_theme_button(self):
        self.find_by_xpath(MenuConstants.DARK_THEME_BUTTON_XPATH).click()

    def click_on_contact_us_button(self):
        self.find_by_xpath(MenuConstants.CONTACT_US_BUTTON_XPATH).click()

    def click_on_logout_button(self):
        self.find_by_xpath(MenuConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(MenuConstants.NO_BUTTON_XPATH).click()

    def click_on_yes_button(self):
        self.find_by_xpath(MenuConstants.YES_BUTTON_XPATH).click()
