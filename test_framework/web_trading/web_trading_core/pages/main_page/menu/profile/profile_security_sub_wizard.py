from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_constants import ProfileConstants


class ProfileSecuritySubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_old_password(self, old_password):
        self.set_text_by_xpath(ProfileConstants.OLD_PASSWORD_FIELD_XPATH, old_password)

    def set_new_password(self, new_password):
        self.set_text_by_xpath(ProfileConstants.NEW_PASSWORD_FIELD_XPATH, new_password)

    def set_confirm_password(self, confirm_password):
        self.set_text_by_xpath(ProfileConstants.CONFIRM_PASSWORD_FIELD_XPATH, confirm_password)
