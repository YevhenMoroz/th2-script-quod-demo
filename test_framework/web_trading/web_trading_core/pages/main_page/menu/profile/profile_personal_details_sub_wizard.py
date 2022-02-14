from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_constants import ProfileConstants


class ProfilePersonalDetailsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def get_first_name(self):
        return self.find_by_xpath(ProfileConstants.FIRST_NAME_FIELD_XPATH).text

    def get_last_name(self):
        return self.find_by_xpath(ProfileConstants.LAST_NAME_FIELD_XPATH).text

    def get_mobile_no(self):
        return self.get_text_by_xpath(ProfileConstants.MOBILE_NO_FIELD_XPATH)

    def get_email(self):
        return self.get_text_by_xpath(ProfileConstants.EMAIL_FIELD_XPATH)

    def get_country(self):
        return self.get_text_by_xpath(ProfileConstants.COUNTRY_FIELD_XPATH)

    def get_address(self):
        return self.get_text_by_xpath(ProfileConstants.ADDRESS_FIELD_XPATH)

    def get_data_of_birth(self):
        return self.get_text_by_xpath(ProfileConstants.DATA_OF_BIRTH_FIELD_XPATH)
