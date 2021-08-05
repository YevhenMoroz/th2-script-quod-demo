import re
import time
from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from selenium.webdriver import ActionChains


class UsersPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)
        self.pattern_for_date = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|' \
                                r'[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:' \
                                r'(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:' \
                                r'(?:1[6-9]|[2-9]\d)?\d{2})$'

    def click_on_new_button(self):
        self.find_by_xpath(UsersConstants.NEW_BUTTON_XPATH).click()

    def click_on_enable_disable_button(self):
        self.find_by_xpath(UsersConstants.ENABLE_DISABLE_BUTTON_XPATH).click()
        time.sleep(2)
        self.find_by_xpath(UsersConstants.OK_BUTTON_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(UsersConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(UsersConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(UsersConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(UsersConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(UsersConstants.PIN_TO_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_ok(self):
        self.find_by_xpath(UsersConstants.OK_BUTTON_XPATH).click()

    def offset_horizontal_slide(self):
        slider = self.find_by_xpath(UsersConstants.HORIZONTAL_SCROLL)
        action = ActionChains(self.web_driver_container.get_driver())
        action.drag_and_drop_by_offset(slider, 400, 0).perform()

    # set for filters
    def set_user_id(self, value):
        self.set_text_by_xpath(UsersConstants.USER_ID_FILTER_AT_MAIN_PAGE, value)

    def set_first_name(self, value):
        self.set_text_by_xpath(UsersConstants.FIRST_NAME_FILTER_AT_MAIN_PAGE, value)

    def set_last_name(self, value):
        self.set_text_by_xpath(UsersConstants.LAST_NAME_FILTER_AT_MAIN_PAGE, value)

    def set_ext_id_client(self, value):
        self.set_text_by_xpath(UsersConstants.EXT_ID_CLIENT_FILTER_AT_MAIN_PAGE, value)

    def set_ext_id_venue(self, value):
        self.set_text_by_xpath(UsersConstants.EXT_ID_VENUE_FILTER_AT_MAIN_PAGE, value)

    def set_password_expiry_date(self, value):
        match = re.fullmatch(self.pattern_for_date, value)
        if match:
            self.set_text_by_xpath(UsersConstants.PASSWORD_EXPIRY_DATE_FILTER_AT_MAIN_PAGE, value)
        else:
            print("Incorrect date value, please use this format - day/month/year")
            raise classmethod.__name__

    def set_first_login(self, value):
        self.set_combobox_value(UsersConstants.FIRST_LOGIN_FILTER_AT_MAIN_PAGE, value)

    def set_ping(self, value):
        self.set_combobox_value(UsersConstants.PING_FILTER_AT_MAIN_PAGE, value)

    def set_address(self, value):
        self.set_text_by_xpath(UsersConstants.ADDRESS_FILTER_AT_MAIN_PAGE, value)

    def set_country(self, value):
        self.set_text_by_xpath(UsersConstants.COUNTRY_FILTER_AT_MAIN_PAGE, value)

    def set_birth_date(self, value):
        match = re.fullmatch(self.pattern_for_date, value)
        if match:
            self.set_text_by_xpath(UsersConstants.BIRTH_DATE_FILTER_AT_MAIN_PAGE, value)
        else:
            print("Incorrect date value, please use this format - day/month/year")
            raise classmethod.__name__

    def set_extension(self, value):
        self.set_text_by_xpath(UsersConstants.EXTENSION_FILTER_AT_MAIN_PAGE, value)

    def set_mobile(self, value):
        self.set_text_by_xpath(UsersConstants.MOBILE_FILTER_AT_MAIN_PAGE, value)

    def set_email(self, value):
        self.set_text_by_xpath(UsersConstants.EMAIL_FILTER_AT_MAIN_PAGE, value)

    def set_enabled(self, value):
        self.set_combobox_value(UsersConstants.ENABLED_FILTER_AT_MAIN_PAGE, value)

    def set_locked(self, value):
        self.set_combobox_value(UsersConstants.LOCKED_FILTER_AT_MAIN_PAGE, value)

    def set_connected(self, value):
        self.set_combobox_value(UsersConstants.CONNECTED_FILTER_AT_MAIN_PAGE, value)

    def get_disabled_massage(self):
        return self.find_by_xpath(UsersConstants.DISABLED_MESSAGE).text

    def get_user_id(self):
        return self.find_by_xpath(UsersConstants.USER_ID_AT_MAIN_PAGE).text

    def get_first_name(self):
        return self.find_by_xpath(UsersConstants.FIRST_NAME_AT_MAIN_PAGE).text

    def get_last_name(self):
        return self.find_by_xpath(UsersConstants.LAST_NAME_AT_MAIN_PAGE).text

    def get_ext_id_client(self):
        return self.find_by_xpath(UsersConstants.EXT_ID_CLIENT_AT_MAIN_PAGE).text

    def get_ext_id_venue(self):
        return self.find_by_xpath(UsersConstants.EXT_ID_VENUE_AT_MAIN_PAGE).text

    def get_password_expiry_date(self):
        return self.find_by_xpath(UsersConstants.PASSWORD_EXPIRY_DATE_AT_MAIN_PAGE).text

    def get_first_login(self):
        return self.find_by_xpath(UsersConstants.FIRST_LOGIN_AT_MAIN_PAGE).text

    def get_ping(self):
        return self.find_by_xpath(UsersConstants.PING_AT_MAIN_PAGE).text

    def get_address(self):
        return self.find_by_xpath(UsersConstants.ADDRESS_AT_MAIN_PAGE).text

    def get_country(self):
        return self.find_by_xpath(UsersConstants.COUNTRY_AT_MAIN_PAGE).text

    def get_birth_date(self):
        return self.find_by_xpath(UsersConstants.BIRTH_AT_MAIN_PAGE).text

    def get_extension(self):
        return self.find_by_xpath(UsersConstants.EXTENSION_AT_MAIN_PAGE).text

    def get_mobile(self):
        return self.find_by_xpath(UsersConstants.MOBILE_AT_MAIN_PAGE).text

    def get_email(self):
        return self.find_by_xpath(UsersConstants.EMAIL_AT_MAIN_PAGE).text

    def get_enabled(self):
        return self.find_by_xpath(UsersConstants.ENABLED_AT_MAIN_PAGE).text

    def get_locked(self):
        return self.find_by_xpath(UsersConstants.LOCKED_AT_MAIN_PAGE).text

    def get_connected(self):
        return self.find_by_xpath(UsersConstants.CONNECTED_AT_MAIN_PAGE).text
