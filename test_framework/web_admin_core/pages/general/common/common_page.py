import time
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.general.common.common_constants import CommonConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
import pyperclip

class CommonPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_refresh_button(self):
        self.find_by_xpath(CommonConstants.REFRESH_PAGE_XPATH).click()

    def click_on_download_csv_button(self):
        self.find_by_xpath(CommonConstants.DOWNLOAD_CSV_XPATH).click()

    def click_on_send_feedback_button(self):
        self.find_by_xpath(CommonConstants.SEND_FEEDBACK_BUTTON_XPATH).click()

    def set_text_to_feedback_text_area(self, value):
        self.set_text_by_xpath(CommonConstants.SEND_FEEDBACK_TEXT_AREA_XPATH, value)

    def click_on_send_button_at_feedback_area(self):
        self.find_by_xpath(CommonConstants.SEND_FEEDBACK_SEND_BUTTON_XPATH).click()

    def click_on_logout(self):
        self.find_by_xpath(CommonConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CommonConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def set_old_password_at_login_page(self, value):
        self.set_text_by_xpath(CommonConstants.OLD_PASSWORD_FIELD_AT_LOGIN_PAGE_XPATH, value)

    def set_new_password_at_login_page(self, value):
        self.set_text_by_xpath(CommonConstants.NEW_PASSWORD_FIELD_AT_LOGIN_PAGE_XPATH, value)

    def click_on_dark_theme(self):
        self.find_by_xpath(CommonConstants.DARK_THEME_XPATH).click()

    def click_on_help_icon(self):
        self.find_by_xpath(CommonConstants.HELP_ICON_XPATH).click()

    def click_on_help_icon_at_login_page(self):
        self.find_by_xpath(CommonConstants.HELP_ICON_AT_LOGIN_PAGE_XPATH).click()

    def refresh_page(self):
        self.find_by_xpath(CommonConstants.REFRESH_PAGE_XPATH).click()

    def is_user_name_icon_displayed(self):
        return "logged-in-user ng-star-inserted" == self.find_by_xpath(CommonConstants.USER_NAME_XPATH).get_attribute(
            "class")

    def is_help_icon_displayed(self):
        return "icon-container ng-star-inserted" == self.find_by_xpath(CommonConstants.HELP_ICON_XPATH).get_attribute(
            "class")

    def is_send_feedback_icon_displayed(self):
        return "Send Feedback to Quod Financial" == self.find_by_xpath(
            CommonConstants.SEND_FEEDBACK_BUTTON_XPATH).get_attribute("nbtooltip")

    def is_send_button_at_feedback_area_disabled_enabled(self):
        return self.find_by_xpath(CommonConstants.SEND_FEEDBACK_SEND_BUTTON_XPATH).is_enabled()

    def is_header_displayed(self):
        return self.is_element_present(CommonConstants.HEADER_XPATH)

    def is_user_icon_displayed(self):
        return "control-item icon-btn context-menu-host" == self.find_by_xpath(
            CommonConstants.USER_ICON_AT_RIGHT_CORNER).get_attribute("class")

    def click_on_full_screen_button(self):
        self.find_by_xpath(CommonConstants.FULL_SCREEN_BUTTON_XPATH).click()

    def click_on_exit_full_screen_button(self):
        self.find_by_xpath(CommonConstants.EXIT_FULL_SCREEN_BUTTON_XPATH).click()

    def click_on_esc_keyboard_button(self):
        self.use_keyboard_esc_button()

    def click_on_copy_version_button(self):
        self.find_by_xpath(CommonConstants.COPY_VERSION_BUTTON).click()

    def extract_version_from_copy_version(self):
        self.click_on_copy_version_button()
        time.sleep(1)
        element = pyperclip.paste()
        print(element)
        return element

    def click_on_about(self):
        self.find_by_xpath(CommonConstants.ABOUT_BUTTON_XPATH).click()

    def extract_admin_version(self):
        return self.find_by_xpath(CommonConstants.ADMIN_VERSION_XPATH).text

    def click_on_application_information_at_send_feedback(self):
        self.find_by_xpath(CommonConstants.APPLICATION_INFORMATION_AT_SEND_FEEDBACK_XPATH).click()

    def click_on_arrow_back_button_at_send_feedback(self):
        self.find_by_xpath(CommonConstants.ARROW_BACK_BUTTON_XPATH).click()

    def get_user_id_at_send_feedback(self):
        return self.find_by_xpath(CommonConstants.USER_ID_AT_SEND_FEEDBACK_ADDITION_INFORMATION).text

    def is_send_feedback_field_displayed(self):
        return self.is_element_present(CommonConstants.SEND_FEEDBACK_SEND_BUTTON_XPATH)

    def is_link_of_help_icon_correct(self, link):
        window_after = self.web_driver_container.get_driver().window_handles[1]
        self.web_driver_container.get_driver().switch_to.window(window_after)
        inst = self.web_driver_container.get_driver().current_url
        return link == inst
