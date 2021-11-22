from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class FeesCommissionProfilePointsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(FeesConstants.COMMISSION_PROFILE_POINTS_PLUS_BUTTON_XPATH).click()

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
