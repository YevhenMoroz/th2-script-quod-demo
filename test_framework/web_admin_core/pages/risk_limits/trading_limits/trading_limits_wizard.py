import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.trading_limits.trading_limits_constants import \
    TradingLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class TradingLimitsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(TradingLimitsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(TradingLimitsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(TradingLimitsConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(TradingLimitsConstants.GO_BACK_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(TradingLimitsConstants.OK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(TradingLimitsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                TradingLimitsConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def get_footer_warning_text(self):
        return self.find_by_xpath(TradingLimitsConstants.FOOTER_WARNING_TEXT_XPATH).text
