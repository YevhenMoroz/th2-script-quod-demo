from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.general.admin_command.admin_command_constants import AdminCommandConstants
from quod_qa.web_admin.web_admin_core.pages.general.common.common_constants import CommonConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommonPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_refresh_button(self):
        self.find_by_xpath(CommonConstants.REFRESH_PAGE_XPATH).click()

    def click_on_download_csv_button(self):
        self.find_by_xpath(CommonConstants.DOWNLOAD_CSV_XPATH).click()


    def click_on_send_feedback_button(self):
        self.find_by_xpath(CommonConstants.SEND_FEEDBACK_BUTTON_XPATH).click()

    def set_text_to_feedback_text_area(self,value):
        self.set_text_by_xpath(CommonConstants.SEND_FEEDBACK_TEXT_AREA_XPATH,value)

    def click_on_send_button_at_feedback_area(self):
        self.find_by_xpath(CommonConstants.SEND_FEEDBACK_SEND_BUTTON_XPATH).click()

    def click_on_logout(self):
        self.find_by_xpath(CommonConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CommonConstants.USER_ICON_AT_RIGHT_CORNER).click()

