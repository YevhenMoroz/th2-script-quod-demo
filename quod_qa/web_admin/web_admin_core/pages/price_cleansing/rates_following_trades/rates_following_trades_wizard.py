import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.price_cleansing.rates_following_trades.rates_following_trades_constants import \
    RatesFollowingTradesConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class RatesFollowingTradesWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(RatesFollowingTradesConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(RatesFollowingTradesConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(RatesFollowingTradesConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(RatesFollowingTradesConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(RatesFollowingTradesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                RatesFollowingTradesConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False
