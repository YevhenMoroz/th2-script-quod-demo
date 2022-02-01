from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_constants import ProfileConstants


class ProfilePage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_personal_details_button(self):
        self.find_by_xpath(ProfileConstants.PERSONAL_DETAILS_BUTTON_XPATH).click()

    def click_on_preference_button(self):
        self.find_by_xpath(ProfileConstants.PREFERENCE_BUTTON_XPATH).click()

    def click_on_security_button(self):
        self.find_by_xpath(ProfileConstants.SECURITY_BUTTON_XPATH)

    def click_on_terms_and_condition_button(self):
        self.find_by_xpath(ProfileConstants.TERMS_AND_CONDITION_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(ProfileConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_save_button(self):
        self.find_by_xpath(ProfileConstants.SAVE_BUTTON_XPATH).click()
