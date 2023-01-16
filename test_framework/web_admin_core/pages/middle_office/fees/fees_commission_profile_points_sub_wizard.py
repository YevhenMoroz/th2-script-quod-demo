from selenium.webdriver import ActionChains
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class FeesCommissionProfilePointsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        element = self.find_by_xpath(FeesConstants.COMMISSION_PROFILE_POINTS_PLUS_BUTTON_XPATH)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element)
        action.click()
        action.perform()

    def click_on_close(self):
        self.find_by_xpath(FeesConstants.COMMISSION_PROFILE_POINTS_CANCEL_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(FeesConstants.COMMISSION_PROFILE_POINTS_CHECKMARK_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(FeesConstants.COMMISSION_PROFILE_POINTS_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(FeesConstants.COMMISSION_PROFILE_POINTS_DELETE_BUTTON_XPATH).click()

    def set_base_value(self, value):
        self.set_text_by_xpath(FeesConstants.COMMISSION_PROFILE_BASE_VALUE_XPATH, value)

    def get_base_value(self):
        return self.get_text_by_xpath(FeesConstants.COMMISSION_PROFILE_BASE_VALUE_XPATH)

    def set_min_commission(self, value):
        self.set_text_by_xpath(FeesConstants.COMMISSION_PROFILE_MIN_COMMISSION_XPATH, value)

    def get_min_commission(self):
        return self.get_text_by_xpath(FeesConstants.COMMISSION_PROFILE_MIN_COMMISSION_XPATH)

    def set_upper_limit(self, value):
        self.set_text_by_xpath(FeesConstants.COMMISSION_PROFILE_UPPER_LIMIT_XPATH, value)

    def get_upper_limit(self):
        return self.get_text_by_xpath(FeesConstants.COMMISSION_PROFILE_UPPER_LIMIT_XPATH)

    def get_all_upper_limit_values_from_table(self):
        return self.get_all_items_from_table_column(FeesConstants.UPPER_LIMIT_COLUMN_XPATH)

    def set_slope(self, value):
        self.set_text_by_xpath(FeesConstants.COMMISSION_PROFILE_SLOPE_XPATH, value)

    def get_slope(self):
        return self.get_text_by_xpath(FeesConstants.COMMISSION_PROFILE_SLOPE_XPATH)
