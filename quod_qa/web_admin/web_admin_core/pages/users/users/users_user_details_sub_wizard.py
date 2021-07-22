from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class UsersUserDetailsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_first_name(self, value):
        self.set_text_by_xpath(UsersConstants.FIRST_NAME_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_first_name(self):
        return self.get_text_by_xpath(UsersConstants.FIRST_NAME_AT_USER_DETAILS_SUB_WIZARD)

    def set_last_name(self, value):
        self.set_text_by_xpath(UsersConstants.LAST_NAME_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_last_name(self):
        return self.get_text_by_xpath(UsersConstants.LAST_NAME_AT_USER_DETAILS_SUB_WIZARD)

    def set_address(self, value):
        self.set_text_by_xpath(UsersConstants.ADDRESS_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_address(self):
        return self.get_text_by_xpath(UsersConstants.ADDRESS_AT_USER_DETAILS_SUB_WIZARD)

    def set_mail(self, value):
        self.set_text_by_xpath(UsersConstants.MAIL_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_mail(self):
        return self.get_text_by_xpath(UsersConstants.MAIL_AT_USER_DETAILS_SUB_WIZARD)

    def set_extension(self, value):
        self.set_text_by_xpath(UsersConstants.EXTENSION_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_extension(self):
        self.get_text_by_xpath(UsersConstants.EXTENSION_AT_USER_DETAILS_SUB_WIZARD)

    def set_mobile(self, value):
        self.set_text_by_xpath(UsersConstants.MOBILE_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_mobile(self):
        return self.get_text_by_xpath(UsersConstants.MOBILE_AT_USER_DETAILS_SUB_WIZARD)

    def set_country(self, value):
        self.set_text_by_xpath(UsersConstants.COUNTRY_AT_USER_DETAILS_SUB_WIZARD, value)

    def get_country(self):
        return self.get_text_by_xpath(UsersConstants.COUNTRY_AT_USER_DETAILS_SUB_WIZARD)

    def set_date_of_birth(self, value):
        self.set_text_by_xpath(UsersConstants.DATE_OF_BIRTH, value)

    def get_date_of_birth(self):
        return self.get_text_by_xpath(UsersConstants.DATE_OF_BIRTH)
