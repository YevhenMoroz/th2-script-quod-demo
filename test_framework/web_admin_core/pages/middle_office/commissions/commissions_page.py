import time

from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_constants import CommissionsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CommissionsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(CommissionsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CommissionsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(CommissionsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(CommissionsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(CommissionsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(CommissionsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CommissionsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(CommissionsConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(CommissionsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CommissionsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(CommissionsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(CommissionsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_instr_type(self, value):
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_INSTR_TYPE_FILTER_XPATH, value)

    def set_venue(self, value):
        self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_VENUE_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_side(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_SIDE_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_SIDE_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_SIDE_FILTER_XPATH, value)

    def set_execution_policy(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_EXECUTION_POLICY_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_EXECUTION_POLICY_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_EXECUTION_POLICY_FILTER_XPATH, value)

    def set_virtual_account(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_VIRTUAL_ACCOUNT_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_VIRTUAL_ACCOUNT_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_VIRTUAL_ACCOUNT_FILTER_XPATH, value)

    def set_client(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_CLIENT_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_CLIENT_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_client_group(self, value):
        self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)

    def set_client_list(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_CLIENT_LIST_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_CLIENT_LIST_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_CLIENT_LIST_FILTER_XPATH, value)

    def set_commission_amount_type(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_COMMISSION_AMOUNT_TYPE_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_COMMISSION_AMOUNT_TYPE_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_COMMISSION_AMOUNT_TYPE_FILTER_XPATH, value)

    def set_commission_profile(self, value):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_COMMISSION_PROFILE_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_COMMISSION_PROFILE_FILTER_XPATH)
        self.set_text_by_xpath(CommissionsConstants.MAIN_PAGE_COMMISSION_PROFILE_FILTER_XPATH, value)

    def click_on_re_calculate_for_allocations(self):
        if not self.is_element_present(CommissionsConstants.MAIN_PAGE_RE_CALCULATE_FOR_ALLOCATIONS_FILTER_XPATH):
            self.horizontal_scroll(CommissionsConstants.MAIN_PAGE_RE_CALCULATE_FOR_ALLOCATIONS_FILTER_XPATH)
        self.find_by_xpath(CommissionsConstants.MAIN_PAGE_RE_CALCULATE_FOR_ALLOCATIONS_FILTER_XPATH).click()

    def offset_horizontal_slide(self):
        scr_elem = self.find_by_xpath(CommissionsConstants.HORIZONTAL_SCROLL)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element_with_offset(scr_elem, scr_elem.size["width"]-5, 5)
        action.click()
        action.perform()