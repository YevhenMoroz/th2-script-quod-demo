from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.users.user_sessions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_user_name_filter(self, value):
        self.set_text_by_xpath(Constants.MainPage.USER_NAME_FILTER, value)

    def click_on_active_button(self, confirm: bool = None):
        self.find_by_xpath(Constants.MainPage.ACTIVE_BUTTON).click()
        if confirm:
            self.find_by_xpath(Constants.MainPage.OK_BUTTON).click()
        elif not confirm:
            self.find_by_xpath(Constants.MainPage.CANCEL_BUTTON).click()
